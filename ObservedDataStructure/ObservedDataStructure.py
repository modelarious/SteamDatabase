from dataclasses import asdict
from typing import List
from QueueEntries.Sendable import Sendable
from Server.SocketWrapper import SocketWrapper

# Observer pattern, but sending updates over a socket
class ObservedDataStructure:
    # func will be one of this class' methods
    def sendUpdateDecorator(func):
        # updates socket after performing an action
        def update_sock(self, *args, **kwargs):
            func(self, *args, **kwargs)
            messageToSend = list(self.dict.values())
            # if you want to sort here, you'll need to be able to handle a list
            # of strings or a list of dicts (the models converted to dictionaries)
            self.socketToUpdate.send_message(messageToSend)
        return update_sock

    @sendUpdateDecorator
    def __init__(self, socketToUpdate : SocketWrapper):
        self.socketToUpdate = socketToUpdate
        self.dict = {}
    
    @sendUpdateDecorator
    def add(self, sendable: Sendable):
        self._add(sendable)

    @sendUpdateDecorator
    def remove(self, sendable: Sendable):
        del self.dict[sendable.game_name_on_disk]
    
    @sendUpdateDecorator
    def batch_add(self, sendables: List[Sendable]):
        for sendable in sendables:
            self._add(sendable)

    def _add(self, sendable: Sendable):
        self.dict[sendable.game_name_on_disk] = asdict(sendable)
    