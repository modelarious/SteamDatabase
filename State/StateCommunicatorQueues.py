from State.StateCommunicatorInterface import StateCommunicatorInterface
from threading import Thread
from Constants import END_OF_QUEUE

#type hints
from typing import Any
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from GameModel import Game
from queue import Queue

from dataclasses import dataclass

# XXX note that it would be great to be able to define type of 
# payload as "Queuable" instead of "Any"
@dataclass
class QueueItem:
    functionName: str
    payload: Any

import inspect
from typing import List
class StateCommunicationQueueWriter(StateCommunicatorInterface): 
    # can't find a way to express this properly in type checking. 
    # Technically, queue is a multiprocessing.managers.AutoProxy[Queue]
    def __init__(self, queue: Queue):
        self.queue = queue

    def _putOnQueue(self, payload: Any):
        funcName = self._determine_function_name()
        queueItem = QueueItem(funcName, payload)
        # print(f"[{funcName}] - {payload}")
        self.queue.put(queueItem)

    def batchSetUpcomingState(self, gameTitlesOnDisk : List[str]):
        self._putOnQueue(gameTitlesOnDisk)
  
    def setFindingNameActiveState(self, gameTitleOnDisk : str):
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
            funcName = queueItem.functionName
            instance_method = getattr(self.stateCommunicator, funcName)
            instance_method(queueItem.payload)
            queueItem = self.queue.get()
            