
from Server.SocketWrapper import SocketWrapper

# Observer pattern, but sending updates over a socket
class ObservedDataStructure:

    # func will be one of this class' methods
    def sendUpdateDecorator(func):
        # updates socket after performing an action
        def update_sock(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.socketToUpdate.send_message(self.set)
        return update_sock

    @sendUpdateDecorator
    def __init__(self, socketToUpdate : SocketWrapper):
        self.socketToUpdate = socketToUpdate
        self.set = set()
    
    @sendUpdateDecorator
    def add(self, value):
        self.set.add(value)

    @sendUpdateDecorator
    def remove(self, value):
        self.set.remove(value)