from State.StateCommunicatorQueues import StateCommunicationQueueWriter
from CommandDispatch.CommandConstants import COMMAND_NAME
from Server.SocketWrapper import SocketWrapper

from abc import ABC, abstractmethod
from typing import Dict, Any, Callable

class Command(ABC):
    def __init__(self, message: Dict[str, Any], state_communicator: StateCommunicationQueueWriter, input_socket_fetch_function: Callable[[], SocketWrapper]):
        self.command_name = message[COMMAND_NAME]
        self.state_communicator = state_communicator
        self.input_socket_fetch_function = input_socket_fetch_function

    @abstractmethod
    def execute(self):
        pass

    def get_command_name(self):
        return self.command_name