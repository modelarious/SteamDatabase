from Server.SocketWrapper import SocketWrapper
from threading import Event
from enum import Enum

UPCOMING_STATE = '/upcoming'

expectedSockets = set([
    UPCOMING_STATE
])

class WebsocketClientHandlerRegistry:
    def __init__(self):
        self.socketWrappers = dict()
        self.allSocketsReady = Event()

    def _internalCheckAllSocketsReady(self):
        if set(self.socketWrappers.keys()) == expectedSockets:
            #signal to any processes waiting for configuration
            self.allSocketsReady.set()
    
    def track_socket_and_loop(self, socket, socket_name):
        wrapped_socket = SocketWrapper(socket, socket_name)
        self.socketWrappers[socket_name] = wrapped_socket
        self._internalCheckAllSocketsReady()

        # loop until client closes connection
        wrapped_socket.connection_loop()

        # client has closed connection, so stop tracking it
        del self.socketWrappers[socket_name]
    
    def get_socket(self, socket_name):
        return self.socketWrappers[socket_name]