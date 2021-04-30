from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from Server.Server import Server

from State.StateCommunicatorFactory import StateCommunicatorFactory
from State.ObserverSocketHookupFactory import ObserverSocketHookupFactory
from State.StateCommunicatorInterface import StateCommunicatorInterface

from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from GameModel import Game

class ServerProxyObject(StateCommunicatorInterface):
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
    
    # XXX it would be easy to make a mistake writing this.
    # XXX Is there a different way to expose the self.stateCommunicator api directly?
    def setUpcomingState(self, gameTitleOnDisk : str):
        self.stateCommunicator.setUpcomingState(gameTitleOnDisk)
    
    def setFindingNameActiveState(self, gameTitleOnDisk : str):
        self.stateCommunicator.setFindingNameActiveState(gameTitleOnDisk)
    
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry : UserInputRequiredQueueEntry):
        self.stateCommunicator.setAwaitingUserInputState(userInputRequiredQueueEntry)
    
    def rejectedByUser(self, userInputRequiredQueueEntry: UserInputRequiredQueueEntry):
        self.stateCommunicator.rejectedByUser(userInputRequiredQueueEntry)
    
    def setQueuedForInfoRetrievalState(self, matchQueueEntry : MatchQueueEntry):
        self.stateCommunicator.setQueuedForInfoRetrievalState(matchQueueEntry)
    
    def setInfoRetrievalActiveState(self, matchQueueEntry : MatchQueueEntry):
        self.stateCommunicator.setInfoRetrievalActiveState(matchQueueEntry)
    
    def setStoredState(self, game : Game):
        self.stateCommunicator.setStoredState(game)
