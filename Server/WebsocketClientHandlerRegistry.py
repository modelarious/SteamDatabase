from Server.SocketWrapper import SocketWrapper

class WebsocketClientHandlerRegistry:
    def __init__(self):
        self.socketWrappers = dict()
    
    def track_socket_and_loop(self, socket, socket_name):
        wrapped_socket = SocketWrapper(socket, socket_name)
        self.socketWrappers[socket_name] = wrapped_socket

        # loop until client closes connection
        wrapped_socket.connection_loop()

        # client has closed connection, so stop tracking it
        del self.socketWrappers[socket_name]
    
    def get_socket(self, socket_name):
        return self.socketWrappers[socket_name]