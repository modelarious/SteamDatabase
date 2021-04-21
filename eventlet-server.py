from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from Server.Server import Server
from multiprocessing.managers import BaseManager

from State.StateCommunicatorFactory import StateCommunicatorFactory
from State.ObserverSocketHookupFactory import ObserverSocketHookupFactory
from State.StateCommunicator import StateCommunicator

class ServerProxyObject:
    def __init__(self):
        websocketRegistry = WebsocketClientHandlerRegistry()
        server = Server(websocketRegistry)
        server.startInThread()

        print("waiting on sockets")
        websocketRegistry.waitForAllSocketsReady()
        print("all needed sockets have been connected")

        # now that we are guaranteed that the sockets are connected, we can use them
        observerSocketHookupFactory = ObserverSocketHookupFactory(websocketRegistry)
        stateCommunicatorFactory = StateCommunicatorFactory()
        self.stateCommunicator = stateCommunicatorFactory.createStateCommunicator(observerSocketHookupFactory)
    
    # Can't do this because it would require serializing the StateCommunicator which 
    # would require serializing sockets which makes no sense
    # def getStateCommunicator(self) -> StateCommunicator:
    #     return self.stateCommunicator
    
    def sendMessage(self, string):
        self.stateCommunicator.setUpcomingState(string)

if __name__ == '__main__':
    # websocketRegistry = WebsocketClientHandlerRegistry()
    # server = Server(websocketRegistry)
    # server.startInThread()

    # print("waiting on sockets")
    # websocketRegistry.waitForAllSocketsReady()
    # print("all needed sockets have been connected")

    # # now that we are guaranteed that the sockets are connected, we can use them
    # observerSocketHookupFactory = ObserverSocketHookupFactory(websocketRegistry)
    # stateCommunicatorFactory = StateCommunicatorFactory()
    # stateCommunicator = stateCommunicatorFactory.createStateCommunicator(observerSocketHookupFactory)

    class ShareObjectBetweenProcesses(BaseManager):  
        pass
  
    ShareObjectBetweenProcesses.register('ServerProxyObject', ServerProxyObject) 
    shareObjectBetweenProcesses = ShareObjectBetweenProcesses()  
    shareObjectBetweenProcesses.start()  
    serverProxyObject = shareObjectBetweenProcesses.ServerProxyObject()
    print(serverProxyObject)

    serverProxyObject.sendMessage("hello")

    # from time import sleep
    # stateCommunicator.setUpcomingState('factorio')
    # sleep(1)
    # stateCommunicator.setUpcomingState('satisfactory')
    # sleep(3)
    # stateCommunicator.setFindingNameActiveState('factorio')
    # sleep(3)
    # stateCommunicator.setFindingNameActiveState('satisfactory')
    shareObjectBetweenProcesses.join()

