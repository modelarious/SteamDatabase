from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from ObservedDataStructure.ObservedDataStructure import ObservedDataStructure


class ObserverSocketHookupFactory:
    def __init__(self, websocketRegistry: WebsocketClientHandlerRegistry):
        self.websocketRegistry = websocketRegistry

    # socket name should be one of the states in States.py
    def hookUpObservableDataStructure(self, socketName: str) -> ObservedDataStructure:
        def fetchSocket():
            return self.websocketRegistry.get_socket(socketName)

        return ObservedDataStructure(fetchSocket, socketName)
