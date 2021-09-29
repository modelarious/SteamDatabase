from Server.SocketWrapper import SocketWrapper
from threading import Event
from State.States import STATES

# socket is used for issuing commands from front end to back end
COMMAND = '/command'
GAMES = '/games'


# GAMES_SUMMARY = '/games_summary' # Would be nice to do
# select steam_id, header_image_url from appdetails;
# to get a summary of the games instead of sending ALL THE DATA EVER
# XXX Extending the above, when sending to the debug view it would be nice to just send the Sendable and SteamSendable
# objects instead of the full sized objects to cut down on network traffic

expectedSockets = set([
    COMMAND,
    GAMES
])

# add all States to expectedSockets
expectedSockets |= STATES

class WebsocketClientHandlerRegistry:
    def __init__(self):
        self.__socketWrappers = dict()
        self.__allSocketsReady = Event()
        self._internalCheckAllSocketsReady()

    def waitForAllSocketsReady(self):
        self.__allSocketsReady.wait()

    def track_socket_and_loop(self, socket, socket_name):
        if socket_name in self.__socketWrappers:
            self.__socketWrappers[socket_name].replace_socket(socket)
        else:
            wrapped_socket = SocketWrapper(socket, socket_name)
            self.__socketWrappers[socket_name] = wrapped_socket

        self._internalCheckAllSocketsReady()

        # loop until client closes connection
        self.__socketWrappers[socket_name].connection_loop()

        # client has closed connection
        # self.__socketWrappers[socket_name].mark_closed()
    
    def get_socket(self, socket_name):
        return self.__socketWrappers[socket_name]
    
    def _internalCheckAllSocketsReady(self):
        currentSockets = set(self.__socketWrappers.keys())
        if currentSockets == expectedSockets:
            #signal to any processes waiting for configuration
            self.__allSocketsReady.set()
        else:
            print(f"waiting for {expectedSockets.difference(currentSockets)}")