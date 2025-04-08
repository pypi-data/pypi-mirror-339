
#################################################
# HolAdo (Holistic Automation do)
#
# (C) Copyright 2021-2025 by Eric Klumpp
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# The Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.
#################################################

import logging
import socket
from _socket import SHUT_RDWR
from holado.common.handlers.object import DeleteableObject
import abc
from holado_core.common.exceptions.functional_exception import FunctionalException
from holado_core.common.tools.tools import Tools
from holado_python.standard_library.ssl.ssl import SslManager
import threading
import types
from abc import abstractmethod
from holado.common.handlers.undefined import undefined_argument

logger = logging.getLogger(__name__)


class Socket(DeleteableObject):
    """
    Base class for socket objects.
    
    It is implemented internally with standard library socket.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None, idle_sleep_delay=undefined_argument):
        """Socket constructor
        @param name: Socket name
        @param create_ipv4_socket_kwargs: arguments to create an IPv4 socket
        @param idle_sleep_delay: delay to sleep when socket is idle (used in some clients/servers to control CPU resource impact ; default: 0.01 s)
        """
        if name is None and create_ipv4_socket_kwargs is not None:
            if not set(create_ipv4_socket_kwargs.keys()).issuperset({'host', 'port'}):
                raise FunctionalException(f"Parameters 'host' and 'port' must be defined")
            name = f"{create_ipv4_socket_kwargs['host']}:{create_ipv4_socket_kwargs['port']}"
        
        super().__init__(name)
        self.__socket = None
        self.__is_started = False
        self.__start_thread = None
        self.__idle_sleep_delay = idle_sleep_delay if idle_sleep_delay is not undefined_argument else 0.01
        
        # SSL management
        self.__is_with_ssl = False
        self.__is_ssl_handshake_done = False
        
        if create_ipv4_socket_kwargs is not None:
            self.create_ipv4_socket(**create_ipv4_socket_kwargs)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _delete_object(self):
        self.close()
    
    @property    
    def internal_socket(self) -> socket.socket:
        return self.__socket
    
    @property
    def is_started(self):
        return self.__is_started
    
    @property
    def is_with_ssl(self):
        return self.__is_with_ssl
    
    @property
    def _idle_sleep_delay(self):
        return self.__idle_sleep_delay
    
    def _set_internal_socket(self, socket, is_with_ssl=False, is_ssl_handshake_done_on_connect=True):
        self.__socket = socket
        self.__is_with_ssl = is_with_ssl
        self.__is_ssl_handshake_done = is_ssl_handshake_done_on_connect
    
    @abc.abstractmethod
    def create_ipv4_socket(self, host, port, **kwargs):
        raise NotImplementedError()
    
    def close(self):
        if self.__socket is not None:
            try:
                self.__socket.shutdown(SHUT_RDWR)
            except OSError as exc:
                if 'Errno 107' in str(exc):
                    logger.info(f"Got following error on socket shutdown (known to appear sometimes during shutdown): {exc}")
                else:
                    raise exc
            finally:
                self.__socket.close()
                self.__socket = None
    
    @abstractmethod
    def start(self, *, read_bufsize=1024, read_kwargs=None, write_kwargs=None):
        raise NotImplementedError()
    
    def _start_thread(self, thread):
        # Start thread
        self.__start_thread = thread
        self.__start_thread.start()
        self.__is_started = True
        
        if Tools.do_log(logger, logging.DEBUG):
            logger.debug(f"[{self.name}] Started")
    
    def stop(self):
        if self.__start_thread is not None:
            if self.__start_thread.is_interruptable:
                self.__start_thread.interrupt()
            self.__start_thread.join()
            self.__start_thread = None
            self.__is_started = False
            
            if Tools.do_log(logger, logging.DEBUG):
                logger.debug(f"[{self.name}] Stopped")
    
    def read(self, bufsize=1024, **kwargs):
        flags = kwargs.get('flags', 0)
        res = self.internal_socket.recv(bufsize, flags)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"[{self.name}] Received [{res}] (type: {type(res)})")
        return res
    
    def write(self, data_bytes, loop_until_all_is_sent=True, **kwargs):
        if loop_until_all_is_sent:
            # Note: no return is done, since sendall return None or raise an exception on error
            self.internal_socket.sendall(data_bytes, **kwargs)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"[{self.name}] Sent all [{data_bytes}] (type: {type(data_bytes)})")
        else:
            res = self.internal_socket.send(data_bytes, **kwargs)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"[{self.name}] Sent {res}/{len(data_bytes)} bytes of [{data_bytes}] (type: {type(data_bytes)})")
            return res
    
    def _new_ssl_context_if_required(self, server_side=False, **socket_kwargs):
        """Return a SSLContext if required, and the remaining socket kwargs.
        """
        res = None
        if Tools.has_sub_kwargs(socket_kwargs, 'ssl.'):
            ssl_kwargs = Tools.pop_sub_kwargs(socket_kwargs, 'ssl.')
            res = SslManager.new_ssl_context(server_side=server_side, flat_kwargs=ssl_kwargs)
        return res, socket_kwargs
    
    def do_ssl_handshake(self):
        # Handshake management is performed differently with blocking or non-blocking connection
        # See BlockingSocketClient and NonBlockingSocketClient for implementation
        raise NotImplementedError()
    
    def ensure_ssl_handshake_is_done(self):
        if self.is_with_ssl and not self.__is_ssl_handshake_done:
            self.do_ssl_handshake()
            self.__is_ssl_handshake_done = True


class SocketClient(Socket):
    """
    Base class for socket clients.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None, idle_sleep_delay=undefined_argument, do_run_with_recv=True, do_run_with_send=True):
        """Socket client constructor
        @param name: Socket client name
        @param create_ipv4_socket_kwargs: Arguments to create an IPv4 socket
        @param idle_sleep_delay: delay to sleep when socket is idle (used only in some clients to control CPU resource impact ; default: 0.01 s)
        @param do_run_with_recv: Define if recv is done in run process when client is started
        @param do_run_with_send: Define if send is done in run process when client is started
        """
        # Data used in start processing
        self.__data_lock = threading.Lock()
        self.__data = types.SimpleNamespace(
            in_bytes=b"",
            out_bytes=b"",
        )
        self.__with_recv = do_run_with_recv
        self.__with_send = do_run_with_send
        
        # Note: super().__init__ must be done after self.__data & others initialization since it can execute create_ipv4_socket_kwargs method
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs, idle_sleep_delay=idle_sleep_delay)
    
    @property
    def is_run_with_recv(self):
        return self.__with_recv
    
    @property
    def is_run_with_send(self):
        return self.__with_send
    
    @property
    def _data_lock(self):
        return self.__data_lock
    
    @property
    def _data(self):
        return self.__data
    
    def _delete_object(self):
        self.stop()
        super()._delete_object()
    
    def _start_thread(self, thread):
        # Ensure SSL handshake is done before starting to receive and send data
        self.ensure_ssl_handshake_is_done()
        
        # Start thread
        super()._start_thread(thread)
    
    @property
    def received_data_size(self):
        with self.__data_lock:
            res = len(self.__data.in_bytes)
        return res
    
    def read(self, bufsize=1024, **kwargs):
        if self.is_started and self.is_run_with_recv:
            with self.__data_lock:
                if self.__data.in_bytes:
                    res = self.__data.in_bytes[:bufsize]
                    self.__data.in_bytes = self.__data.in_bytes[bufsize:]
                else:
                    res = b''
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f"[{self.name}] Read data from received data: [{res}] (type: {type(res)} ; remaining data: {len(self.__data.in_bytes)})")
            return res
        else:
            return super().read(bufsize=bufsize, **kwargs)
    
    def write(self, data_bytes, loop_until_all_is_sent=True, **kwargs):
        if self.is_started and self.is_run_with_send:
            with self.__data_lock:
                self.__data.out_bytes += data_bytes
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f"[{self.name}] Added data in data to send (total: {len(self.__data.out_bytes)})")
        else:
            return super().write(data_bytes, loop_until_all_is_sent=loop_until_all_is_sent, **kwargs)


class SocketServer(Socket):
    """
    Base class for socket servers.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None, idle_sleep_delay=undefined_argument):
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs, idle_sleep_delay=idle_sleep_delay)
    
    def accept(self):
        conn, addr = self.internal_socket.accept()
        res = Socket(name=f"[{self.name}] Connection with {addr}")
        res._set_internal_socket(conn)
        return res, addr
    
    @abc.abstractmethod
    def _process_received_data(self, data):
        raise NotImplementedError()



