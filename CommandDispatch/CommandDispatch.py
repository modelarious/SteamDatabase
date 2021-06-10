from CommandDispatch.CommandFactory import CommandFactory
from CommandDispatch.CommandConstants import SHUTDOWN_COMMAND
from Server.SocketWrapper import SocketWrapper

class CommandDispatch:
    def __init__(self, command_socket: SocketWrapper, command_factory: CommandFactory):
        self.command_socket = command_socket
        self.command_factory = command_factory

    def command_loop(self):
        while True:
            print("awaiting command")
            message = self.command_socket.get_message()
            command = self.command_factory.create(message)

            if command.get_command_name() == SHUTDOWN_COMMAND:
                break

            # blocking
            command.execute()
        print("shut down command dispatcher")