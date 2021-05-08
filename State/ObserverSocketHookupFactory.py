from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from State.ObservedDataStructure import ObservedDataStructure
from multiprocessing import Manager

class ObserverSocketHookupFactory:
    def __init__(self, websocketRegistry: WebsocketClientHandlerRegistry):
        self.websocketRegistry = websocketRegistry

    # socket name should be one of the states in States.py
    def hookUpObservableDataStructure(self, socketName: str) -> ObservedDataStructure:
        socket = self.websocketRegistry.get_socket(socketName)
        return ObservedDataStructure(socket)