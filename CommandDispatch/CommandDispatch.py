from CommandDispatch.CommandFactory import CommandFactory
from CommandDispatch.CommandConstants import SHUTDOWN_COMMAND
from Server.SocketWrapper import SocketWrapper
from typing import Callable

class CommandDispatch:
    def __init__(self, command_socket_fetch_function: Callable[[], SocketWrapper], command_factory: CommandFactory):
        self.command_socket_fetch_function = command_socket_fetch_function
        self.command_factory = command_factory

    def command_loop(self):
        while True:
            print("awaiting command")
            command_socket = self.command_socket_fetch_function()
            message = command_socket.get_message()

            print("Got message:", message)
            if message == "init":
                continue
            
            # XXX maybe message will be None because the socket disconnects?
            command = self.command_factory.create(message)

            if command.get_command_name() == SHUTDOWN_COMMAND:
                break

            # blocking
            command.execute()
        print("shut down command dispatcher")