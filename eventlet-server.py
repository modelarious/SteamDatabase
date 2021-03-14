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

# provides an interface to access the 
class SocketWrapper:
    def __init__(self, socket, socket_name):
        self.socket = socket
        self.socket_name = socket_name
        self.received_message_queue = Queue()
    
    def wait(self):
        received_message = self.socket.wait()
        self.received_message_queue.put(received_message)
        return received_message

    def get_message(self):
        return self.received_message_queue.get()
    
    def send_message(self, content):
        print(f"updating {self.socket_name} with {content}")
        self.socket.send(str(content))
    
    def connection_loop(self):
        while True:
            received_message = self.wait()
            # if the client closed the connection, break out
            if received_message == None:
                return

class WebsocketClientHandler:
    def __init__(self):
        self.socketWrappers = dict()
    
    def track_socket(self, socket, socket_name):
        wrapped_socket = SocketWrapper(socket, socket_name)
        self.socketWrappers[socket_name] = wrapped_socket
        wrapped_socket.connection_loop()
    
    def get_socket(self, socket_name):
        return self.socketWrappers[socket_name]


def server_function():
    websocketClientHandler = WebsocketClientHandler()

    def server(websocketClientHandler):

        # this blocks and fills a queue with messages received from the socket
        @websocket.WebSocketWSGI
        def socket_collector(ws):
            print(ws.path)
            websocketClientHandler.track_socket(ws, ws.path)

        wsgi.server(eventlet.listen(('', 8091)), socket_collector)

    serverThread = Thread(target=server, args = (websocketClientHandler,))
    serverThread.start()
    sleep(10)

    GAME_SOCKET = '/game'

    gameSock = websocketClientHandler.get_socket(GAME_SOCKET)

    gameSock.send_message('oh')
    gameSock.send_message('yeah')
    gameSock.send_message('biiiiiitch')

    while True:
        print("top of loop")
        print(gameSock.get_message())
        sleep(5)
        

    serverThread.join()


from threading import Thread
from time import sleep
if __name__ == '__main__':
    server_function()
