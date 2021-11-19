from multiprocessing import Process, Condition, Lock  
from multiprocessing.managers import BaseManager  
import time, os  
  

# NEed to know
# Will hosting this as a manager destroy the ability to communicate through the sockets?
# Will the local lock inside the ObservedDataStructure be respected by multiple processes?
  
class observedD(object):  
    def __init__(self):  
        self.nl = []
        lock = Lock()
      
    def getLen(self):  
        return len(self.nl)  
      
    def stampa(self):  
        print(self.nl)
          
    def appendi(self, x):  
        self.nl.append(x)  
      
    def svuota(self):  
        for i in range(len(self.nl)):  
            del self.nl[0]  
      

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


class StateCommunicator:
    def __init__(self, connections : Dict[StateStrType, ObservedDataStructure]):

        self.previousState = {}

        # doing this with helpful names so accesses in member functions are easy to read
        self.upcoming  = connections[UPCOMING_STATE]
        self.findingNameActive = connections[FINDING_NAME_ACTIVE_STATE]
        self.awaitingUser = connections[AWAITING_USER_STATE]
        self.queuedForInfoRetrieval = connections[QUEUED_FOR_INFO_RETRIEVAL_STATE]
        self.infoRetrievalActive = connections[INFO_RETRIEVAL_ACTIVE_STATE]
        self.stored = connections[STORED]

    def setUpcomingState(self, gameTitleOnDisk : str):
        self.upcoming.add(gameTitleOnDisk)
        self._trackCurrentState(self.upcoming, gameTitleOnDisk)
    
    def setFindingNameActiveState(self, gameTitleOnDisk : str):
        self.upcoming.remove(gameTitleOnDisk)
        self.findingNameActive.add(gameTitleOnDisk)
        self._trackCurrentState(self.findingNameActive, gameTitleOnDisk)
    
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry : UserInputRequiredQueueEntry):
        gameTitleOnDisk = userInputRequiredQueueEntry.getGameName()
        self.findingNameActive.remove(gameTitleOnDisk)
        self.awaitingUser.add(userInputRequiredQueueEntry.toDict(), gameTitleOnDisk)
        self._trackCurrentState(self.awaitingUser, gameTitleOnDisk)
    
    def transitionToErrorState(self, gameTitle: str):
        self.awaitingUser.remove(gameTitle)
    
    def setQueuedForInfoRetrievalState(self, matchQueueEntry : MatchQueueEntry):
        gameTitleOnDisk = matchQueueEntry.getGameNameOnDisk()

        # Could have been a 100% name match in which case, previous state was FindingNameActiveState.
        # Also could have been only a partial match to a few names and the user had to select
        # the correct one, so the previous state was AwaitingUserInputState.
        prevState = self._getPreviousState(gameTitleOnDisk)
        prevState.remove(gameTitleOnDisk)

        self.queuedForInfoRetrieval.add(matchQueueEntry.toDict(), gameTitleOnDisk)
        self._trackCurrentState(self.queuedForInfoRetrieval, gameTitleOnDisk)
    
    def setInfoRetrievalActiveState(self, matchQueueEntry : MatchQueueEntry):
        gameTitleOnDisk = matchQueueEntry.getGameNameOnDisk()
        self.queuedForInfoRetrieval.remove(gameTitleOnDisk)

        self.infoRetrievalActive.add(matchQueueEntry.toDict(), gameTitleOnDisk)
        self._trackCurrentState(self.infoRetrievalActive, gameTitleOnDisk)
    
    def setStoredState(self, game : Game):
        gameTitleOnDisk = game.name_on_harddrive
        self.infoRetrievalActive.remove(gameTitleOnDisk)
        self.stored.add(game.toDict(), gameTitleOnDisk)
        self._trackCurrentState(self.stored, gameTitleOnDisk)
    
    def _trackCurrentState(self, state: ObservedDataStructure, gameTitleOnDisk: str):
        self.previousState[gameTitleOnDisk] = state
        
    def _getPreviousState(self, gameTitleOnDisk: str):
        return self.previousState[gameTitleOnDisk]

    

class ShareObjectBetweenProcesses(BaseManager):  
    pass  
  
ShareObjectBetweenProcesses.register('StateCommunicator', StateCommunicator, 
    exposed = [
        'setUpcomingState', 
        'setFindingNameActiveState', 
        'setAwaitingUserInputState', 
        'transitionToErrorState', 
        'setQueuedForInfoRetrievalState', 
        'setInfoRetrievalActiveState', 
        'setStoredState'
    ]
)  
  
def consume(waitC, waitP, listaNumeri):  
    lock.acquire()  
    if (listaNumeri.getLen() == 0):  
        waitC.wait()  
    listaNumeri.stampa()  
    listaNumeri.svuota()  
    waitP.notify()  
    lock.release()  
      
def produce(waitC, waitP, listaNumeri):  
    lock.acquire()  
    if (listaNumeri.getLen() > 0):  
        waitP.wait()  
    for i in range(10):  
        listaNumeri.appendi(i)  
    waitC.notify()  
    lock.release()  
  
      
def main():  
    mymanager = ShareObjectBetweenProcesses()  
    mymanager.start()  
    stateCommunicator = ShareObjectBetweenProcesses.stateCommunicator()

    producer = Process(target = produce, args =(waitC, waitP, stateCommunicator,))  
    producer.start()  
    time.sleep(2)  
    consumer = Process(target = consume, args =(waitC, waitP, stateCommunicator,))  
    consumer.start()

    mymanager.join()
    producer.join()
    consumer.join()
  
main()