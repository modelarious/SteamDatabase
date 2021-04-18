from Server.SocketWrapper import SocketWrapper

# Observer pattern, but sending updates over a socket
class ObservedDataStructure:
    # func will be one of this class' methods
    def sendUpdateDecorator(func):
        # updates socket after performing an action
        def update_sock(self, *args, **kwargs):
            func(self, *args, **kwargs)
            messageToSend = list(self.dict.values())
            sortedMessage = sorted(messageToSend)
            self.socketToUpdate.send_message(sortedMessage)
        return update_sock

    @sendUpdateDecorator
    def __init__(self, socketToUpdate : SocketWrapper):
        self.socketToUpdate = socketToUpdate
        self.dict = {}
    
    @sendUpdateDecorator
    def add(self, value, key=None):
        if key == None:
            key = value
        self.dict[key] = value

    @sendUpdateDecorator
    def remove(self, key):
        del self.dict[key]
