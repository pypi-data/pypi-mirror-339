#
#  Copyright (c) 2011-2014 Exxeleron GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import socket
import struct
import ssl
import json

from qconnect import MetaData, CONVERSION_OPTIONS
from qconnect.qtype import QException
from qconnect.qreader import QReader, QReaderException
from qconnect.qwriter import QWriter, QWriterException
from qconnect.oauth import retrieve_tokens_AZURE_pkce, retrieve_tokens_AZURE_client_credentials

class QConnectionException(Exception):
    '''Raised when a connection to the q service cannot be established.'''
    pass

class QAuthenticationException(QConnectionException):
    '''Raised when a connection to the q service is denied.'''
    pass


class MessageType(object):
    '''Enumeration defining IPC protocol message types.'''
    ASYNC = 0
    SYNC = 1
    RESPONSE = 2



class QConnection(object):
    '''Connector class for interfacing with the q service.
    
    Provides methods for synchronous and asynchronous interaction.
    
    The :class:`.QConnection` class provides a context manager API and can be 
    used with a ``with`` statement::
    
        with qconnection.QConnection(host = 'localhost', port = 5000) as q:
            print(q)
            print(q('{`int$ til x}', 10))
    
    :Parameters:
     - `host` (`string`) - q service hostname
     - `port` (`integer`) - q service port
     - `username` (`string` or `None`) - username for q authentication/authorization
     - `password` (`string` or `None`) - password for q authentication/authorization
     - `timeout` (`nonnegative float` or `None`) - set a timeout on blocking socket operations
     - `tls_enabled` (`True`False or `None) - set tls_enabled to use TLS Handshake and SSL Encryption
     - `encoding` (`string`) - string encoding for data deserialization
     - `reader_class` (subclass of `QReader`) - data deserializer
     - `writer_class` (subclass of `QWriter`) - data serializer
     - `custom_ca` (`string` or `None`) - hardcoded path to custom ca cert if required
    :Options: 
     - `raw` (`boolean`) - if ``True`` returns raw data chunk instead of parsed 
       data, **Default**: ``False``
     - `numpy_temporals` (`boolean`) - if ``False`` temporal vectors are
       backed by raw q representation (:class:`.QTemporalList`, 
       :class:`.QTemporal`) instances, otherwise are represented as 
       `numpy datetime64`/`timedelta64` arrays and atoms,
       **Default**: ``False``
     - `single_char_strings` (`boolean`) - if ``True`` single char Python 
       strings are encoded as q strings instead of chars, **Default**: ``False``
    '''

    MAX_PROTOCOL_VERSION = 6

    def __init__(self,
                 host,
                 port,
                 username=None,
                 password=None,
                 timeout = None,
                 oauth_provider=None,
                 oauth_config=None,
                 tls_enabled=True,
                 encoding='latin-1',
                 reader_class = None,
                 writer_class = None,
                 custom_ca=None,
                 **options):
        """
        :param oauth_provider: One of ['azure', ....], or None
        :param oauth_config: A dict or custom object with keys like:
                            {
                              "tenant_id": "...",
                              "client_id": "...",
                              "client_secret": "...",  # if you are using "client_credentials" flow
                              "scope": "api://xyz/.read_data",
                              "flow": "pkce" or "client_credentials",
                              "redirect_port": xxxx # optional in pkce if you prefer to not use port 5000 for the temporary server
                            }
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.oauth_provider = oauth_provider
        self.oauth_config = oauth_config or {}
        self.tokens = {}
        self.tls_enabled = tls_enabled
        self.custom_ca = custom_ca

        self._connection = None
        self._connection_file = None
        self._protocol_version = None

        self.timeout = timeout

        self._encoding = encoding

        self._options = MetaData(**CONVERSION_OPTIONS.union_dict(**options))

        try:
            from qconnect._pandas import PandasQReader, PandasQWriter
            self._reader_class = PandasQReader
            self._writer_class = PandasQWriter
        except ImportError:
            self._reader_class = QReader
            self._writer_class = QWriter

        if reader_class:
            self._reader_class = reader_class

        if writer_class:
            self._writer_class = writer_class

                # Initialize SSL context
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.check_hostname = True
        self.context.load_default_certs()

        # Append custom CA if provided
        if self.custom_ca:
            self.append_custom_ca(self.custom_ca)


    def append_custom_ca(self, ca_path):
        """Append a custom CA certificate to the SSL context."""
        try:
            self.context.load_verify_locations(cafile=ca_path)
            print(f"Custom CA certificate loaded from: {ca_path}")
        except Exception as e:
            print(f"Failed to load custom CA certificate from {ca_path}: {e}")


    def __enter__(self):
        self.open()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    @property
    def protocol_version(self):
        '''Retrieves established version of the IPC protocol.
        
        :returns: `integer` -- version of the IPC protocol
        '''
        return self._protocol_version


    def open(self):
        '''Initialises connection to q service.
        
        If the connection hasn't been initialised yet, invoking the 
        :func:`.open` creates a new socket and performs a handshake with a q 
        service.
        
        :raises: :class:`.QConnectionException`, :class:`.QAuthenticationException` 
        '''
        if not self._connection:
            if not self.host:
                raise QConnectionException('Host cannot be None')

            if self.oauth_provider == 'azure':
                flow = self.oauth_config.get("flow", "client_credentials")
                if flow == "pkce":
                    self.tokens = retrieve_tokens_AZURE_pkce(TENANT_ID = self.oauth_config.get("tenant_id", ""),
                                                        CLIENT_ID = self.oauth_config.get("client_id", ""),
                                                        KDB_SCOPE = self.oauth_config.get("scope", ""),
                                                        tokens = self.tokens,
                                                        REDIRECT_PORT = self.oauth_config.get("redirect_port", 5000))
                    self._effective_password = self.tokens["access_token"]
                elif flow == "client_credentials":
                    self.tokens = retrieve_tokens_AZURE_client_credentials(TENANT_ID = self.oauth_config.get("tenant_id", ""),
                                                        CLIENT_ID = self.oauth_config.get("client_id", ""),
                                                        CLIENT_SECRET = self.oauth_config.get("client_secret", ""),
                                                        KDB_SCOPE = self.oauth_config.get("scope", ""),
                                                        tokens = self.tokens)
                    self._effective_password = self.tokens["access_token"]
                else:
                    raise Exception(f"Unknown OAuth flow: {flow}")
            else:
                # Basic Auth / or no auth
                self._effective_password = self.password

            self._init_socket()
            self._initialize()

            self._writer = self._writer_class(self._connection, protocol_version = self._protocol_version, encoding = self._encoding)
            self._reader = self._reader_class(self._connection_file, encoding = self._encoding)


    def _init_socket(self):
        '''Initialises the socket used for communicating with a q service,'''
        try:
            self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if self.tls_enabled:
                self._connection = self.context.wrap_socket(self._connection,server_hostname = self.host)

            self._connection.settimeout(self.timeout)
            self._connection.connect((self.host, self.port))
            self._connection_file = self._connection.makefile('b')
        except:
            self._connection = None
            self._connection_file = None
            raise


    def close(self):
        '''Closes connection with the q service.'''
        if self._connection:
            self._connection_file.close()
            self._connection_file = None
            self._connection.close()
            self._connection = None


    def is_connected(self):
        '''Checks whether connection with a q service has been established. 
        
        Connection is considered inactive when: 
         - it has not been initialised, 
         - it has been closed.
         
        :returns: `boolean` -- ``True`` if connection has been established, 
                  ``False`` otherwise
        '''
        return True if self._connection else False


    def _initialize(self):
        '''Performs a IPC protocol handshake.'''
        credentials = (self.username if self.username else '') + ':' + (self._effective_password if self._effective_password else '')
        credentials = credentials.encode(self._encoding)
        self._connection.send(credentials + bytes([self.MAX_PROTOCOL_VERSION, 0]))
        response = self._connection.recv(1)

        if len(response) != 1:
            self.close()
            self._init_socket()

            self._connection.send(credentials + b'\0')
            response = self._connection.recv(1)
            if len(response) != 1:
                self.close()
                raise QAuthenticationException('Connection denied.')

        self._protocol_version = min(struct.unpack('B', response)[0], self.MAX_PROTOCOL_VERSION)


    def __str__(self):
        return '%s@:%s:%s' % (self.username, self.host, self.port) if self.username else ':%s:%s' % (self.host, self.port)


    def query(self, msg_type, query, *parameters, **options):
        '''Performs a query against a q service.
        
        In typical use case, `query` is the name of the function to call and 
        `parameters` are its parameters. When `parameters` list is empty, the 
        query can be an arbitrary q expression (e.g. ``0 +/ til 100``).
        
        Calls a anonymous function with a single parameter:
        
            >>> q.query(qconnection.MessageType.SYNC,'{til x}', 10)
        
        Executes a q expression:
        
            >>> q.query(qconnection.MessageType.SYNC,'til 10')
        
        :Parameters:
         - `msg_type` (one of the constants defined in :class:`.MessageType`) -
           type of the query to be executed
         - `query` (`string`) - query to be executed
         - `parameters` (`list` or `None`) - parameters for the query
        :Options:
         - `single_char_strings` (`boolean`) - if ``True`` single char Python 
           strings are encoded as q strings instead of chars, 
           **Default**: ``False``
        
        :raises: :class:`.QConnectionException`, :class:`.QWriterException`
        '''
        if not self._connection:
            raise QConnectionException('Connection is not established.')

        if parameters and len(parameters) > 8:
            raise QWriterException('Too many parameters.')

        # Convert any dictionary parameters to JSON strings
        processed_params = []
        for param in parameters:
            if isinstance(param, dict):
                processed_params.append(json.dumps(param))
            else:
                processed_params.append(param)

        if not parameters or len(parameters) == 0:
            self._writer.write(query, msg_type, **self._options.union_dict(**options))
        else:
            self._writer.write([query] + processed_params, msg_type, **self._options.union_dict(**options))


    def sendSync(self, query, *parameters, **options):
        '''Performs a synchronous query against a q service and returns parsed 
        data.
        
        In typical use case, `query` is the name of the function to call and 
        `parameters` are its parameters. When `parameters` list is empty, the 
        query can be an arbitrary q expression (e.g. ``0 +/ til 100``).
        
        Executes a q expression:
        
            >>> print(q.sendSync('til 10'))
            [0 1 2 3 4 5 6 7 8 9]
        
        Executes an anonymous q function with a single parameter:
        
            >>> print(q.sendSync('{til x}', 10))
            [0 1 2 3 4 5 6 7 8 9]
            
        Executes an anonymous q function with two parameters:
        
            >>> print(q.sendSync('{y + til x}', 10, 1))
            [ 1  2  3  4  5  6  7  8  9 10]
            
            >>> print(q.sendSync('{y + til x}', *[10, 1]))
            [ 1  2  3  4  5  6  7  8  9 10]
        
        The :func:`.sendSync` is called from the overloaded :func:`.__call__` 
        function. This allows :class:`.QConnection` instance to be called as 
        a function:
        
            >>> print(q('{y + til x}', 10, 1))
            [ 1  2  3  4  5  6  7  8  9 10]
        
        
        :Parameters:
         - `query` (`string`) - query to be executed
         - `parameters` (`list` or `None`) - parameters for the query
        :Options: 
         - `raw` (`boolean`) - if ``True`` returns raw data chunk instead of 
           parsed data, **Default**: ``False``
         - `numpy_temporals` (`boolean`) - if ``False`` temporal vectors are
           backed by raw q representation (:class:`.QTemporalList`, 
           :class:`.QTemporal`) instances, otherwise are represented as 
           `numpy datetime64`/`timedelta64` arrays and atoms,
           **Default**: ``False``
         - `single_char_strings` (`boolean`) - if ``True`` single char Python 
           strings are encoded as q strings instead of chars, 
           **Default**: ``False``

        :returns: query result parsed to Python data structures
        
        :raises: :class:`.QConnectionException`, :class:`.QWriterException`, 
                 :class:`.QReaderException`
        '''
        self.query(MessageType.SYNC, query, *parameters, **options)
        response = self.receive(data_only = False, **options)

        if response.type == MessageType.RESPONSE:
            return response.data
        else:
            self._writer.write(QException('nyi: qconnect expected response message'), MessageType.ASYNC if response.type == MessageType.ASYNC else MessageType.RESPONSE)
            raise QReaderException('Received message of type: %s where response was expected')


    def sendAsync(self, query, *parameters, **options):
        '''Performs an asynchronous query and returns **without** retrieving of 
        the response.
        
        In typical use case, `query` is the name of the function to call and 
        `parameters` are its parameters. When `parameters` list is empty, the 
        query can be an arbitrary q expression (e.g. ``0 +/ til 100``).
        
        Calls a anonymous function with a single parameter:
        
            >>> q.sendAsync('{til x}', 10)
        
        Executes a q expression:
        
            >>> q.sendAsync('til 10')
        
        :Parameters:
         - `query` (`string`) - query to be executed
         - `parameters` (`list` or `None`) - parameters for the query
        :Options: 
         - `single_char_strings` (`boolean`) - if ``True`` single char Python 
           strings are encoded as q strings instead of chars, 
           **Default**: ``False``
        
        :raises: :class:`.QConnectionException`, :class:`.QWriterException`
        '''
        self.query(MessageType.ASYNC, query, *parameters, **options)


    def receive(self, data_only = True, **options):
        '''Reads and (optionally) parses the response from a q service.
        
        Retrieves query result along with meta-information:
        
            >>> q.query(qconnection.MessageType.SYNC,'{x}', 10)
            >>> print(q.receive(data_only = False, raw = False))
            QMessage: message type: 2, data size: 13, is_compressed: False, data: 10

        Retrieves parsed query result:

            >>> q.query(qconnection.MessageType.SYNC,'{x}', 10)
            >>> print(q.receive(data_only = True, raw = False))
            10

        Retrieves not-parsed (raw) query result:
        
            >>> from binascii import hexlify
            >>> q.query(qconnection.MessageType.SYNC,'{x}', 10)
            >>> print(hexlify(q.receive(data_only = True, raw = True)))
            fa0a000000
                
        :Parameters:
         - `data_only` (`boolean`) - if ``True`` returns only data part of the 
           message, otherwise returns data and message meta-information 
           encapsulated in :class:`.QMessage` instance 
        :Options:
         - `raw` (`boolean`) - if ``True`` returns raw data chunk instead of 
           parsed data, **Default**: ``False``
         - `numpy_temporals` (`boolean`) - if ``False`` temporal vectors are
           backed by raw q representation (:class:`.QTemporalList`, 
           :class:`.QTemporal`) instances, otherwise are represented as 
           `numpy datetime64`/`timedelta64` arrays and atoms,
           **Default**: ``False``
        
        :returns: depending on parameter flags: :class:`.QMessage` instance, 
                  parsed message, raw data 
        :raises: :class:`.QReaderException`
        '''
        result = self._reader.read(**self._options.union_dict(**options))
        return result.data if data_only else result


    def __call__(self, *parameters, **options):
        return self.sendSync(parameters[0], *parameters[1:], **options)
