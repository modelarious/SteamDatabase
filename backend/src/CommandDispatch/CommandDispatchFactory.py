from Server.WebsocketClientHandlerRegistry import (
    WebsocketClientHandlerRegistry,
    COMMAND,
)
from State.StateCommunicatorQueues import StateCommunicationQueueWriter
from CommandDispatch.CommandFactory import CommandFactory
from CommandDispatch.CommandDispatch import CommandDispatch
from State.States import AWAITING_USER_STATE


class CommandDispatchFactory:
    def create(
        self,
        websocket_registry: WebsocketClientHandlerRegistry,
        writer: StateCommunicationQueueWriter,
    ):
        def fetch_command_socket():
            return websocket_registry.get_socket(COMMAND)

        def fetch_input_socket():
            return websocket_registry.get_socket(AWAITING_USER_STATE)

        command_factory = CommandFactory(writer)
        return CommandDispatch(
            fetch_command_socket, fetch_input_socket, command_factory
        )
