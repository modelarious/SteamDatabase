# Observer pattern, but sending updates over a socket
class ObservedDataStructure:
    def sendUpdateDecorator(func):
        # updates socket after performing an action
        def mutation(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.socketToUpdate.send_message(self.set)
        return mutation

    @sendUpdateDecorator
    def __init__(self, socketToUpdate):
        self.socketToUpdate = socketToUpdate
        self.set = set()
    
    @sendUpdateDecorator
    def add(self, value):
        self.set.add(value)

    @sendUpdateDecorator
    def remove(self, value):
        self.set.remove(value)

class DummySocket:
    def __init__(self):
        self.x = 12345
    def send_message(self, message):
        print(message, self.x)


dummySocket = DummySocket()
x = ObservedDataStructure(dummySocket, 23)

x.add("hello")
x.add("hello again")
x.remove("hello")
