from QueueEntries.Sendable import Sendable
from State.StateCommunicatorInterface import StateCommunicatorInterface
from threading import Thread
from Constants import END_OF_QUEUE

#type hints
from typing import List
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from GameModel import Game
from queue import Queue

from dataclasses import dataclass
import inspect

@dataclass
class QueueSendable:
    functionName: str
    payload: Sendable

# place all the set***State() functions onto a single queue to be read one at a time and output to sockets
class StateCommunicationQueueWriter(StateCommunicatorInterface): 
    # can't find a way to express this properly in type checking. 
    # Technically, queue is a multiprocessing.managers.AutoProxy[Queue]
    def __init__(self, queue: Queue):
        self.queue = queue

    # the most important method of this class 
    def _putOnQueue(self, payload: Sendable):
        funcName = self._determine_function_name()
        queueItem = QueueSendable(funcName, payload)
        print(f"[{funcName}] - {payload}")
        self.queue.put(queueItem)

    def batchSetUpcomingState(self, gameTitlesOnDisk : List[Sendable]):
        self._putOnQueue(gameTitlesOnDisk)
  
    def setFindingNameActiveState(self, gameTitleOnDisk : Sendable):
        self._putOnQueue(gameTitleOnDisk)
    
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry : UserInputRequiredQueueEntry):
        self._putOnQueue(userInputRequiredQueueEntry)
    
    def rejectedByUser(self, userInputRequiredQueueEntry: UserInputRequiredQueueEntry):
        self._putOnQueue(userInputRequiredQueueEntry)
    
    def setQueuedForInfoRetrievalStateFromFindingNameActive(self, matchQueueEntry : MatchQueueEntry):
        self._putOnQueue(matchQueueEntry)

    def setQueuedForInfoRetrievalStateFromAwaitingUser(self, matchQueueEntry : MatchQueueEntry):
        self._putOnQueue(matchQueueEntry)
    
    def setInfoRetrievalActiveState(self, matchQueueEntry : MatchQueueEntry):
        self._putOnQueue(matchQueueEntry)
    
    def setStoredState(self, game : Game):
        self._putOnQueue(game)
    
    def _determine_function_name(self):
        return inspect.stack()[2][3]

# one at a time, read QueueSendable objects from the queue and output them to the correct sockets
class StateCommunicationQueueReader:
    # can't find a way to express this properly in type checking. 
    # Technically, queue is a multiprocessing.managers.AutoProxy[Queue]
    def __init__(self, stateCommunicator: StateCommunicatorInterface, queue: Queue):
        self.stateCommunicator = stateCommunicator
        self.queue = queue
    
    def start(self):
        self.thread = Thread(target=self._queue_fetch_loop)
        self.thread.start()
    
    def join(self):
        self.thread.join()

    def _queue_fetch_loop(self):
        queueItem = self.queue.get()
        while queueItem != END_OF_QUEUE:
            # undo the inspect.stack() to find a function name, like setStoredState
            funcName = queueItem.functionName

            # get a handle for that function from the state communicator that actually writes to sockets.
            # this is undoing _putOnQueue from the StateCommunicationQueueWriter
            instance_method = getattr(self.stateCommunicator, funcName)
            instance_method(queueItem.payload)
            queueItem = self.queue.get()
            