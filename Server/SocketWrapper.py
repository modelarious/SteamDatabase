from queue import Queue
from json import dumps, loads

# SetEncoder adapted from https://stackoverflow.com/a/8230505/7520564
# Clean way to encode sets into json objects by transforming them into a list.
# Also handles sorting the list here because it needs to be sorted before it is
# sent.
import json
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return sorted(list(obj))
        return json.JSONEncoder.default(self, obj)

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
        json_message = dumps(content, cls=SetEncoder)
        print(f"updating {self.socket_name} with {json_message}")
        self.socket.send(json_message)
    
    def connection_loop(self):
        while True:
            received_message = self._wait()
            # if the client closed the connection, break out
            if received_message == None:
                return