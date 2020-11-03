import logging
import socketserver

_logger = logging.getLogger(__name__)

_MAGIC_COMMAND = 'get-my-ip'


class TcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        remote_ip, _ = self.client_address
        _logger.debug('Incoming connection from {}'.format(remote_ip))

        command = self.__receive_first_short_line(buffer_size=len(_MAGIC_COMMAND) + 1)
        if command != _MAGIC_COMMAND:
            _logger.debug('Bad magic command: {!r}'.format(command))
            return

        response = '{}\n'.format(self.client_address[0])
        self.request.sendall(response.encode())
        _logger.debug('Answered request')

    def __receive_first_short_line(self, buffer_size) -> str:
        return self.request.recv(buffer_size).decode().rstrip('\n')


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
