from eventlet import wsgi, websocket, listen
from threading import Thread
from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry

class Server:
    def __init__(self, websocketClientHandlerRegistry):
        self.websocketClientHandlerRegistry = websocketClientHandlerRegistry
        self.serverThread = None

    def __server(self):
        # when a websocket connection is opened, this is run.
        @websocket.WebSocketWSGI
        def socket_collector(ws):
            print(ws.path)

            # this blocks and fills a queue with messages received from the socket.
            self.websocketClientHandlerRegistry.track_socket_and_loop(ws, ws.path)

        wsgi.server(listen(('', 8091)), socket_collector)

    def startInThread(self):
        self.serverThread = Thread(target=self.__server)
        self.serverThread.start()
    
    def join(self):
        self.serverThread.join()