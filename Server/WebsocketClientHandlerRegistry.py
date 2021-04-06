from Server.SocketWrapper import SocketWrapper
from threading import Event
from enum import Enum

# socket is used for issuing commands from front end to back end
COMMAND = '/command'

# socket is used for communicating which games are awaiting initial processing
UPCOMING_STATE = '/upcoming'

expectedSockets = set([
    COMMAND,
    UPCOMING_STATE
])

class WebsocketClientHandlerRegistry:
    def __init__(self):
        self.__socketWrappers = dict()
        self.__allSocketsReady = Event()

    def waitForAllSocketsReady(self):
        self.__allSocketsReady.wait()
    
    def track_socket_and_loop(self, socket, socket_name):
        wrapped_socket = SocketWrapper(socket, socket_name)
        self.__socketWrappers[socket_name] = wrapped_socket
        self._internalCheckAllSocketsReady()

        # loop until client closes connection
        wrapped_socket.connection_loop()

        # client has closed connection, so stop tracking it
        del self.__socketWrappers[socket_name]
    
    def get_socket(self, socket_name):
        return self.__socketWrappers[socket_name]
    
    def _internalCheckAllSocketsReady(self):
        if set(self.__socketWrappers.keys()) == expectedSockets:
            #signal to any processes waiting for configuration
            self.__allSocketsReady.set()