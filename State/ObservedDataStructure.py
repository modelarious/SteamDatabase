from Server.SocketWrapper import SocketWrapper
from multiprocessing import Manager

# Observer pattern, but sending updates over a socket
class ObservedDataStructure:
    # func will be one of this class' methods
    def sendUpdateDecorator(func):
        # updates socket after performing an action
        def update_sock(self, *args, **kwargs):
            with self.lock:
                print("acquired", self.socketToUpdate.socket_name)
                func(self, *args, **kwargs)
                messageToSend = list(self.dict.values())
                # XXX if you want to sort here, you'll need to be able to handle a list
                # XXX of strings or a list of dicts (the models converted to dictionaries)
                self.socketToUpdate.send_message(messageToSend)
                print("unacquiring", self.socketToUpdate.socket_name)
        return update_sock

    def __init__(self, socketToUpdate : SocketWrapper, managerInstance: Manager):
        self.socketToUpdate = socketToUpdate
        self.dict = managerInstance.dict()
        self.lock = managerInstance.Lock()
    
    @sendUpdateDecorator
    def add(self, value, key=None):
        if key == None:
            key = value
        self.dict[key] = value

    @sendUpdateDecorator
    def remove(self, key):
        del self.dict[key]
