from typing import Any, Dict
from State.StateCommunicatorQueues import StateCommunicationQueueWriter
from CommandDispatch.CommandConstants import (
    COMMAND_NAME,
    START_GAME_MATCH_COMMAND,
    SHUTDOWN_COMMAND,
)
from CommandDispatch.Commands.StartGameMatchCommand import StartGameMatchCommand
from CommandDispatch.Commands.ShutdownCommand import ShutdownCommand
from CommandDispatch.InvalidCommandException import InvalidCommandException
from Server.SocketWrapper import SocketWrapper
from typing import Callable


class CommandFactory:
    def __init__(self, state_communicator: StateCommunicationQueueWriter):
        self.writer = state_communicator
        self.command_type_map = {
            START_GAME_MATCH_COMMAND: StartGameMatchCommand,
            SHUTDOWN_COMMAND: ShutdownCommand,
        }

    def create(
        self,
        message: Dict[str, Any],
        input_socket_fetch_function: Callable[[], SocketWrapper],
    ):
        string_command = message[COMMAND_NAME]
        if string_command not in self.command_type_map:
            raise InvalidCommandException(
                f"\n'{string_command}' is not one of the available commands.\nAvailable commands: {list(self.command_type_map.keys())}"
            )
        command_class = self.command_type_map[string_command]
        return command_class(message, self.writer, input_socket_fetch_function)
