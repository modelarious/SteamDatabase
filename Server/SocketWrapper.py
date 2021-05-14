from queue import Queue
from json import dumps, loads

# provides an interface to access the socket
class SocketWrapper:
    def __init__(self, socket, socket_name):
        self.socket = socket
        self.socket_name = socket_name
        self.received_message_queue = Queue()
    
    def _wait(self):
        received_message = self.socket.wait()

        # message would be None if client closed the connection unexpectedly
        if received_message != None:
            json_message = loads(received_message)
            print(f"received {json_message} on {self.socket_name}")
            self.received_message_queue.put(json_message)
        
        return received_message

    def get_message(self):
        return self.received_message_queue.get()
    
    def send_message(self, content):
        json_message = dumps(content)
        
        # if self.socket_name != '/upcoming':
        #     print(f"updating {self.socket_name} with {json_message}")
        self.socket.send(json_message)
    
    def connection_loop(self):
        while True:
            received_message = self._wait()
            # if the client closed the connection, break out
            if received_message == None:
                return