from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry, COMMAND
from State.StateCommunicatorQueues import StateCommunicationQueueWriter
from CommandDispatch.CommandFactory import CommandFactory
from CommandDispatch.CommandDispatch import CommandDispatch

class CommandDispatchFactory:
    def create(self, websocket_registry: WebsocketClientHandlerRegistry, writer: StateCommunicationQueueWriter):
        command_socket = websocket_registry.get_socket(COMMAND)
        command_factory = CommandFactory(writer)
        return CommandDispatch(command_socket, command_factory)