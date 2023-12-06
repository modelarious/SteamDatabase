from queue import Queue
from json import dumps, loads
from typing import Any, Dict


# provides an interface to access the socket
class SocketWrapper:
    def __init__(self, socket, socket_name):
        self.socket = socket
        self.socket_name = socket_name
        self.received_message_queue = Queue()
        self.latest_message = ""

    def _wait(self):
        try:
            received_message = self.socket.wait()

            # message would be None if client closed the connection unexpectedly
            if received_message != None:
                json_message = loads(received_message)
                print(f"received {json_message} on {self.socket_name}")
                self.received_message_queue.put(json_message)

            return received_message
        except ConnectionAbortedError as e:
            print(e)
            return None

    def get_message(self) -> Dict[str, Any]:
        return self.received_message_queue.get()

    def send_message(self, message):
        # track message as it comes in so that you can resend the latest message on reconnect
        self.latest_message = message
        json_message = dumps(message)
        try:
            self.socket.send(json_message)

        # on windows - this throws WinError 10038
        except OSError as e:
            print(f"FAILURE TO SEND MESSAGE {e}")

    def connection_loop(self):
        while True:
            received_message = self._wait()

            # if the client closed the connection, break out
            if received_message == None:
                print(f"{self.socket_name} broke out of the loop")
                return

    def replace_socket(self, socket):
        self.socket = socket

        # resend the latest message on reconnect
        if self.latest_message:
            self.send_message(self.latest_message)
