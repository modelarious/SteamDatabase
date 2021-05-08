# THE WAY TO DO THIS
# create a stateCommunicatorQueue (pick a better name) and when they call 
# stateCommunicator.setUpcomingState(x), you add x to a Manager() Queue.
# That queue has a thread that reads from it and applies the changes on a local stateCommunicator

# if that doesn't work - make a state tracking micro service and communicate via kafka queue


from threading import Thread
from Constants import END_OF_QUEUE
from State.StateCommunicatorInterface import StateCommunicatorInterface

class StateCommunicationQueueWriter(StateCommunicatorInterface):
    def __init__(self, upcomingQueue):
        self.upcomingQueue = upcomingQueue
    
    def setUpcomingState(self, x):
        self.upcomingQueue.add(x)

class StateCommunicationQueueReader:
    def __init__(self, stateCommunicator: StateCommunicatorInterface, upcomingQueue):
        self.queueToStateCommunicatorFunctionAssociation = [
            [upcomingQueue, stateCommunicator.setUpcomingState]
        ]
    
    def start(self):
        threads = []
        for queue, func in self.queueToStateCommunicatorFunctionAssociation:
            t = Thread(target=self._apply_func_to_queue_items(), args=(queue, func))
            t.start()
            threads.append(t)
        
        for thread in threads:
            thread.join()

        
    
    def _apply_func_to_queue_items(self, queue, func):
        entry = queue.get()
        while entry != END_OF_QUEUE:
            func(entry)