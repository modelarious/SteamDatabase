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

        # loop until client closes connection
        wrapped_socket.connection_loop()
    
    def get_socket(self, socket_name):
        return self.socketWrappers[socket_name]


class Server:
    def __init__(self, websocketClientHandler):
        self.websocketClientHandler = websocketClientHandler
        self.serverThread = None

    def __server(self):
        # this blocks and fills a queue with messages received from the socket
        @websocket.WebSocketWSGI
        def socket_collector(ws):
            print(ws.path)
            self.websocketClientHandler.track_socket(ws, ws.path)

        wsgi.server(eventlet.listen(('', 8091)), socket_collector)

    def start(self):
        self.serverThread = Thread(target=self.__server)
        self.serverThread.start()
    
    def join(self):
        self.serverThread.join()


from threading import Thread
from time import sleep
if __name__ == '__main__':
    websocketClientHandler = WebsocketClientHandler()
    server = Server(websocketClientHandler)
    server.start()

    # XXX all below is driver code
    sleep(10)

    GAME_SOCKET = '/game'

    gameSock = websocketClientHandler.get_socket(GAME_SOCKET)

    gameSock.send_message('oh')
    gameSock.send_message('yeah')

    # while True:
    print("top of loop")
    print(gameSock.get_message())
    # sleep(5)
    
    print("waiting on server")
    server.join()
