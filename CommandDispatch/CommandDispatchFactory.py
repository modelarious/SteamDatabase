from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry, COMMAND
from State.StateCommunicatorQueues import StateCommunicationQueueWriter
from CommandDispatch.CommandFactory import CommandFactory
from CommandDispatch.CommandDispatch import CommandDispatch


class CommandDispatchFactory:
    def create(self, websocket_registry: WebsocketClientHandlerRegistry, writer: StateCommunicationQueueWriter):

        def fetch_command_socket():
            return websocket_registry.get_socket(COMMAND)

        command_factory = CommandFactory(writer)
        return CommandDispatch(fetch_command_socket, command_factory)