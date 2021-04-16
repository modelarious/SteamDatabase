from Server.SocketWrapper import SocketWrapper

# Observer pattern, but sending updates over a socket
class ObservedDataStructure:

    # func will be one of this class' methods
    def sendUpdateDecorator(func):
        # updates socket after performing an action
        def update_sock(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.socketToUpdate.send_message(self.set.copy())
        return update_sock

    @sendUpdateDecorator
    def __init__(self, socketToUpdate : SocketWrapper):
        self.socketToUpdate = socketToUpdate
        self.set = set()
        self.internalTag = dict()
    
    @sendUpdateDecorator
    def add(self, value):
        self.set.add(value)

    @sendUpdateDecorator
    def remove(self, value):
        self.set.remove(value)
    
    # these don't need the decorator because they don't update the set data structure directly
    def removeByTag(self, tag):
        value = self.internalTag[tag]
        self.remove(value)

    def addByTag(self, tag, value):
        self.internalTag[tag] = value
        self.add(value)
