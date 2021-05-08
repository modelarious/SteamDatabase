# THE WAY TO DO THIS
# create a stateCommunicatorQueue (pick a better name) and when they call 
# stateCommunicator.setUpcomingState(x), you add x to a Manager() Queue.
# That queue has a thread that reads from it and applies the changes on a local stateCommunicator

# if that doesn't work - make a state tracking micro service and communicate via kafka queue
from State.StateCommunicatorInterface import StateCommunicatorInterface
from threading import Thread
from Constants import END_OF_QUEUE


from typing import Dict
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from State.ObservedDataStructure import ObservedDataStructure
from GameModel import Game
from queue import Queue

import inspect
# XXX This is the least DRY class in the whole project :(
class StateCommunicationQueueWriter(StateCommunicatorInterface):  

    # can't find a way to express this properly in type checking. 
    # Technically, queues is a dict of str : multiprocessing.managers.AutoProxy[Queue]
    # the str portion is the name of the function (like "setFindingNameActiveState")
    def __init__(self, queues: Dict[str, Queue]):
        self.queues = queues
    
    def setUpcomingState(self, gameTitleOnDisk : str):
        queueName = self._determine_function_name()
        self.queues[queueName].put(gameTitleOnDisk)
  
    def setFindingNameActiveState(self, gameTitleOnDisk : str):
        queueName = self._determine_function_name()
        self.queues[queueName].put(gameTitleOnDisk)
    
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry : UserInputRequiredQueueEntry):
        queueName = self._determine_function_name()
        self.queues[queueName].put(userInputRequiredQueueEntry)
    
    def rejectedByUser(self, userInputRequiredQueueEntry: UserInputRequiredQueueEntry):
        queueName = self._determine_function_name()
        self.queues[queueName].put(userInputRequiredQueueEntry)
    
    def setQueuedForInfoRetrievalStateFromFindingNameActive(self, matchQueueEntry : MatchQueueEntry):
        queueName = self._determine_function_name()
        self.queues[queueName].put(matchQueueEntry)

    def setQueuedForInfoRetrievalStateFromAwaitingUser(self, matchQueueEntry : MatchQueueEntry):
        queueName = self._determine_function_name()
        self.queues[queueName].put(matchQueueEntry)
    
    def setInfoRetrievalActiveState(self, matchQueueEntry : MatchQueueEntry):
        queueName = self._determine_function_name()
        self.queues[queueName].put(matchQueueEntry)
    
    def setStoredState(self, game : Game):
        queueName = self._determine_function_name()
        self.queues[queueName].put(game)
    
    def _determine_function_name(self):
        return inspect.stack()[1][3]




# class StateCommunicationQueueWriter:
#     def __init__(self, upcomingQueue):
#         self.upcomingQueue = upcomingQueue
    
#     def setUpcomingState(self, x):
#         self.upcomingQueue.put(x)


class StateCommunicationQueueReader:
    # can't find a way to express this properly in type checking. 
    # Technically, queues is a dict of str : multiprocessing.managers.AutoProxy[Queue]
    # the str portion is the name of the function (like "setFindingNameActiveState")
    def __init__(self, stateCommunicator: StateCommunicatorInterface, queues):
        self.queueToStateCommunicatorFunctionAssociation = []
        for methodName, queue in queues.items():
            instance_method = getattr(stateCommunicator, methodName)
            self.queueToStateCommunicatorFunctionAssociation.append(
                [queue, instance_method]
            )
            
        # self.queueToStateCommunicatorFunctionAssociation = [
        #     [upcomingQueue, stateCommunicator.setUpcomingState]
        # ]
    
    def start(self):
        self.threads = []
        for queue, func in self.queueToStateCommunicatorFunctionAssociation:
            t = Thread(target=self._apply_func_to_queue_items, args=(queue, func))
            t.start()
            self.threads.append(t)
    
    def join(self):
        for thread in self.threads:
            thread.join()

    def _apply_func_to_queue_items(self, queue, func):
        entry = queue.get()
        while entry != END_OF_QUEUE:
            func(entry)
            entry = queue.get()
            