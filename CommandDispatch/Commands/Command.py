from State.StateCommunicatorQueues import StateCommunicationQueueWriter
from CommandDispatch.CommandConstants import COMMAND_NAME

from abc import ABC, abstractmethod
from typing import Dict, Any

class Command(ABC):
    def __init__(self, message: Dict[str, Any], state_communicator: StateCommunicationQueueWriter):
        self.command_name = message[COMMAND_NAME]
        self.state_communicator = state_communicator

    @abstractmethod
    def execute(self):
        pass

    def get_command_name(self):
        return self.command_name