"""This is a simple example of running a wsgi application with eventlet.
For a more fully-featured server which supports multiple processes,
multiple threads, and graceful code reloading, see:

http://pypi.python.org/pypi/Spawning/
"""

# import eventlet
# from eventlet import wsgi


# def hello_world(env, start_response):
#     if env['PATH_INFO'] != '/':
#         start_response('404 Not Found', [('Content-Type', 'text/plain')])
#         return ['Not Found\r\n']
#     start_response('200 OK', [('Content-Type', 'text/plain')])
#     return ['Hello, World!\r\n']

# wsgi.server(eventlet.listen(('', 5001)), hello_world)


from eventlet import wsgi, websocket
import eventlet
from queue import Queue

class SocketInfo:
    def __init__(self, socket):
        self.socket = socket
        self.received_message_queue = Queue()

# stores a given websocket 
class WebsocketClientHandler:
    def __init__(self):
        self.sockets = dict()
        self.received_message_queue = Queue()
    
    def track_socket(self, socket, socket_name):
        self.sockets[socket_name] = socket
        self.__connection_loop(socket_name)
    
    def __connection_loop(self, socket_name):        
        socket = self.sockets[socket_name]
        while True:
            received_message = socket.wait()
            self.received_message_queue.put(received_message) # XXX this needs to be stored per socket
            print(received_message)
    
    def send_to_socket(self, socket_name, content):
        print(f"updating {socket_name} with content {content}")
        self.sockets[socket_name].send(str(content))


from threading import Thread
from time import sleep
if __name__ == '__main__':
    connectionStorage = ConnectionStorage()

    def server(connectionStorage):

        # this blocks and fills a queue with messages received from the socket
        @websocket.WebSocketWSGI
        def socket_collector(ws):
            print(ws.path)
            connectionStorage.track_socket(ws, ws.path)

        wsgi.server(eventlet.listen(('', 8091)), socket_collector)

    serverThread = Thread(target=server, args = (connectionStorage,))
    serverThread.start()
    sleep(30)
    # print("writing to sockets /no and /game")
    # print(f"connectionStorage = {connectionStorage}")
    connectionStorage.send_to_socket('/game', 'hello')
    # connectionStorage.send_to_game_socket('hi there')
    # connectionStorage.send_to_no_socket('secret secret')
    # connectionStorage.sockets['/input']
    serverThread.join()
