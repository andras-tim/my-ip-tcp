import logging
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


    def finish(self) -> None:
        _logger.debug('Close socket')


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def start_server(host: str, tcp_port: int):
    server = ThreadedTCPServer((host, tcp_port), TcpHandler)

    _logger.info('Server is listening on {}:{}'.format(*server.server_address))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        _logger.info('Server terminated')
    except:
        _logger.exception('Server abnormally terminated')
