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
class SocketInfo:
    def __init__(self, socket):
        self.socket = socket
        self.received_message_queue = Queue()
    
    def wait(self):
        received_message = self.socket.wait()
        self.received_message_queue.put(received_message)
        return received_message

    def get_message(self):
        return self.received_message_queue.get()
    
    def send_message(self, content):
        self.socket.send(str(content))



# XXX
# The logic here is strange - some deals with the socket itself, other deals with the socket storage
# perhaps you should move the connection loop into the SocketInfo class and rename it to SocketWrapper
# XXX

class WebsocketClientHandler:
    def __init__(self):
        self.socketInfos = dict()
    
    def track_socket(self, socket, socket_name):
        self.socketInfos[socket_name] = SocketInfo(socket)
        self.__connection_loop(socket_name)
    
    def _resolve_socket(self, socket_name):
        return self.socketInfos[socket_name]
    
    def __connection_loop(self, socket_name):        
        socket = self._resolve_socket(socket_name)
        while True:
            received_message = socket.wait()

            # if the client closed the connection, break out
            if received_message == None:
                return
            print(received_message)
    
    def send_to_socket(self, socket_name, content):
        print(f"updating {socket_name} with content {content}")
        socket = self._resolve_socket(socket_name)
        socket.send_message(content)
    
    def get_message(self, socket_name):
        socket = self._resolve_socket(socket_name)
        return socket.get_message()



from threading import Thread
from time import sleep
if __name__ == '__main__':
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
    # print("writing to sockets /no and /game")
    # print(f"connectionStorage = {connectionStorage}")
    websocketClientHandler.send_to_socket('/game', 'hello')
    # connectionStorage.send_to_game_socket('hi there')
    # connectionStorage.send_to_no_socket('secret secret')
    # connectionStorage.sockets['/input']

    while True:
        print("top of loop")
        sleep(5)
        print(websocketClientHandler.get_message('/game'))

    serverThread.join()
