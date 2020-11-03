import logging
import socket
import socketserver
import threading

_logger = logging.getLogger(__name__)

_BUFFER_SIZE = 100
_MAGIC_COMMAND = 'get-my-ip'


class TcpHandler(socketserver.BaseRequestHandler):
    def setup(self) -> None:
        thread = threading.currentThread()
        thread.name = 'Thread_{}:{}'.format(*self.client_address)

        _logger.debug('Incoming connection')

    def handle(self) -> None:
        command = self.request.recv(_BUFFER_SIZE).decode().rstrip('\n')
        if command != _MAGIC_COMMAND:
            _logger.debug('Bad magic command')
            return

        response = '{}\n'.format(self.client_address[0])
        self.request.sendall(response.encode())
        _logger.debug('Remote IP has been sent; waiting for remote close')
        self.__set_keepalive()

        try:
            if self.request.recv(_BUFFER_SIZE) != b'':
                _logger.warning('Unwanted data received')
                return
        except TimeoutError:
            pass

    def finish(self) -> None:
        _logger.debug('Close socket')

    def __set_keepalive(self, after_idle_sec: int = 1, interval_sec: int = 3, max_fails: int = 5):
        _logger.debug('Enable TCP keep-alive')
        self.request.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.request.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
        self.request.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
        self.request.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def start_server(host: str, tcp_port: int):
    server = ThreadedTCPServer((host, tcp_port), TcpHandler)

    _logger.info('Server is listening on {}:{}'.format(*server.server_address))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        _logger.info('Server terminated')
    except:
        _logger.exception('Server abnormally terminated')
