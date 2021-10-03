import inspect
class StateCommunicationQueueWriter(): 
    def putOnQueue(self, payload):
        funcName = self._determine_function_name()
        print(funcName)

    def setUpcomingState(self, gameTitleOnDisk : str):
        self.putOnQueue(gameTitleOnDisk)
  
    def _determine_function_name(self):
        return inspect.stack()[2][3]

x = StateCommunicationQueueWriter()
x.setUpcomingState("hello")