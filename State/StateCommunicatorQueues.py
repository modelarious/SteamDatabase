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
@dataclass
class QueueItem:
    functionName: str
    payload: Any

import inspect
class StateCommunicationQueueWriter(StateCommunicatorInterface): 
    # can't find a way to express this properly in type checking. 
    # Technically, queue is a multiprocessing.managers.AutoProxy[Queue]
    def __init__(self, queue: Queue):
        self.queue = queue

    def putOnQueue(self, payload: Any):
        funcName = self._determine_function_name()
        queueItem = QueueItem(funcName, payload)
        self.queue.put(queueItem)

    def setUpcomingState(self, gameTitleOnDisk : str):
        self.putOnQueue(gameTitleOnDisk)
  
    def setFindingNameActiveState(self, gameTitleOnDisk : str):
        self.putOnQueue(gameTitleOnDisk)
    
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry : UserInputRequiredQueueEntry):
        self.putOnQueue(userInputRequiredQueueEntry)
    
    def rejectedByUser(self, userInputRequiredQueueEntry: UserInputRequiredQueueEntry):
        self.putOnQueue(userInputRequiredQueueEntry)
    
    def setQueuedForInfoRetrievalStateFromFindingNameActive(self, matchQueueEntry : MatchQueueEntry):
        self.putOnQueue(matchQueueEntry)

    def setQueuedForInfoRetrievalStateFromAwaitingUser(self, matchQueueEntry : MatchQueueEntry):
        self.putOnQueue(matchQueueEntry)
    
    def setInfoRetrievalActiveState(self, matchQueueEntry : MatchQueueEntry):
        self.putOnQueue(matchQueueEntry)
    
    def setStoredState(self, game : Game):
        self.putOnQueue(game)
    
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
            