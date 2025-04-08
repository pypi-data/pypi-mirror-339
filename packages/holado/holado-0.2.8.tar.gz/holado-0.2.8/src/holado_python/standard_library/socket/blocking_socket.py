
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
from holado_python.standard_library.socket.socket import SocketClient, SocketServer
import abc
from holado_multitask.multithreading.loopfunctionthreaded import LoopFunctionThreaded
import time
from holado.common.handlers.undefined import undefined_argument

logger = logging.getLogger(__name__)


##########################################################################
## Clients
##########################################################################


class BlockingSocketClient(SocketClient):
    """
    Base class for blocking socket client.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None, idle_sleep_delay=undefined_argument, do_run_with_recv=True, do_run_with_send=True):
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs, idle_sleep_delay=idle_sleep_delay, do_run_with_recv=do_run_with_recv, do_run_with_send=do_run_with_send)
    
    def start(self, *, read_bufsize=1024, read_kwargs=None, write_kwargs=None):
        """Start client event loop.
        """
        if self.is_with_ssl:
            # Set a small timeout, so that recv has a behaviour similar flag MSG_DONTWAIT
            # See _process_recv_send implementation, recv flags are needed to be forced to 0
            if self._idle_sleep_delay is not None:
                self.internal_socket.settimeout(self._idle_sleep_delay)
            else:
                self.internal_socket.settimeout(0.01)
        
        kwargs = {'read_bufsize':read_bufsize, 'read_kwargs':read_kwargs, 'write_kwargs':write_kwargs}
        thread = LoopFunctionThreaded(self._process_recv_send, kwargs=kwargs, register_thread=True, delay_before_run_sec=None)
        self._start_thread(thread)
    
    def _process_recv_send(self, *, read_bufsize=1024, read_kwargs=None, write_kwargs=None):
        has_activity = False
        read_kwargs = read_kwargs if read_kwargs is not None else {}
        write_kwargs = write_kwargs if write_kwargs is not None else {}
        
        recv_data = None
        if self.is_run_with_recv:
            if self.is_with_ssl:
                # ssl doesn't suppôrt flags != 0
                flags = 0
            else:
                # Add flag to not wait data
                flags = read_kwargs.get('flags', 0)
                flags |= socket.MSG_DONTWAIT
            
            try:
                recv_data = self.internal_socket.recv(read_bufsize, flags)
            except (BlockingIOError, TimeoutError):
                # No data to read
                pass
            else:
                if recv_data:
                    has_activity = True
                    with self._data_lock:
                        self._data.in_bytes += recv_data
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug(f"[{self.name}] Received [{recv_data}] (type: {type(recv_data)} ; total: {len(self._data.in_bytes)})")
        
        sent = None
        if self.is_run_with_send:
            with self._data_lock:
                if self._data.out_bytes:
                    has_activity = True
                    sent = self.internal_socket.send(self._data.out_bytes)
                    if sent > 0:
                        self._data.out_bytes = self._data.out_bytes[sent:]
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug(f"[{self.name}] Sent {sent} data (remaining to send: {len(self._data.out_bytes)})")
        
        # Wait before next loop if no data was exchanged
        if not has_activity and self._idle_sleep_delay is not None:
            time.sleep(self._idle_sleep_delay)
    
    def do_ssl_handshake(self):
        if self.is_with_ssl:
            self.internal_socket.do_handshake()


class TCPBlockingSocketClient(BlockingSocketClient):
    """
    TCP socket client.
    """
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None, idle_sleep_delay=undefined_argument, do_run_with_recv=True, do_run_with_send=True):
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs, idle_sleep_delay=idle_sleep_delay, do_run_with_recv=do_run_with_recv, do_run_with_send=do_run_with_send)
    
    def create_ipv4_socket(self, host, port, **kwargs):
        ssl_context, kwargs = self._new_ssl_context_if_required(**kwargs)
        
        sock = socket.create_connection((host, port), **kwargs)
        
        if ssl_context:
            # do_handshake_on_connect = True
            do_handshake_on_connect = False
            sock = ssl_context.wrap_socket(sock, server_hostname=host, do_handshake_on_connect=do_handshake_on_connect)
            self._set_internal_socket(sock, is_with_ssl=True, is_ssl_handshake_done_on_connect=do_handshake_on_connect)
        else:
            self._set_internal_socket(sock)




##########################################################################
## Servers
##########################################################################


class BlockingSocketServer(SocketServer):
    """
    Base class for socket servers.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None, idle_sleep_delay=undefined_argument):
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs, idle_sleep_delay=idle_sleep_delay)
    
    def start(self, read_bufsize=1024, *, read_kwargs=None, write_kwargs=None):
        """Start server to wait a connection, and then listen data, process data, and send result.
        Note: current implementation is simple and supports only one connection at a time.
        """
        kwargs = {'read_bufsize':read_bufsize, 'read_kwargs':read_kwargs, 'write_kwargs':write_kwargs}
        thread = LoopFunctionThreaded(self.wait_and_process_connection, kwargs=kwargs, register_thread=True, delay_before_run_sec=None)
        self._start_thread(thread)
    
    def wait_and_process_connection(self, read_bufsize=1024, *, read_kwargs=None, write_kwargs=None):
        """Wait a connection, and then listen data, process data, and send result.
        Note: current implementation is simple and supports only one connection at a time.
        """
        read_kwargs = read_kwargs if read_kwargs is not None else {}
        write_kwargs = write_kwargs if write_kwargs is not None else {}
        
        conn, _ = self.accept()
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"[{self.name}] New connection: {conn}")
        with conn:
            while True:
                data = conn.read(read_bufsize, **read_kwargs)
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f"[{self.name}] Received: {data}")
                    
                if not data:
                    break
                result = self._process_received_data(data)
                
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f"[{self.name}] Sending: {result}")
                conn.write(result, **write_kwargs)



class TCPBlockingSocketServer(BlockingSocketServer):
    """
    TCP socket server
    """
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None, idle_sleep_delay=undefined_argument):
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs, idle_sleep_delay=idle_sleep_delay)
    
    def create_ipv4_socket(self, host, port, **kwargs):
        ssl_context, kwargs = self._new_ssl_context_if_required(server_side=True, **kwargs)
        
        sock = socket.create_server((host, port), **kwargs)
        
        if ssl_context:
            do_handshake_on_connect = True
            sock = ssl_context.wrap_socket(sock, server_side=True, do_handshake_on_connect=do_handshake_on_connect)
            self._set_internal_socket(sock, is_with_ssl=True, is_ssl_handshake_done_on_connect=do_handshake_on_connect)
        else:
            self._set_internal_socket(sock)

