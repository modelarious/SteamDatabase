from queue import Queue
from json import dumps, loads
from typing import Any, Dict

# XXX REMOVE ALL THIS STUFF FROM BOTH FILES
INIT = "init"

# provides an interface to access the socket
class SocketWrapper:
    def __init__(self, socket, socket_name):
        self.socket = socket
        self.socket_name = socket_name
        self.received_message_queue = Queue()
        self.received_message_queue.put(INIT)
        print(socket_name, self.received_message_queue)
    
    def _wait(self):
        received_message = self.socket.wait()

        # message would be None if client closed the connection unexpectedly
        if received_message != None:
            json_message = loads(received_message)
            print(f"received {json_message} on {self.socket_name}")
            print(f"placing on queue: {self.received_message_queue}")
            self.received_message_queue.put(json_message)
        
        return received_message

    def get_message(self) -> Dict[str, Any]:
        print(f"fetching from {self.received_message_queue}")
        return self.received_message_queue.get()
    
    def send_message(self, content):
        json_message = dumps(content)
        self.socket.send(json_message)
    
    def connection_loop(self):
        while True:
            received_message = self._wait()
            # if the client closed the connection, break out
            if received_message == None:
                return
    
    def replace_socket(self, socket):
        self.socket = socket