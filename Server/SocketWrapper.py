from queue import Queue

# provides an interface to access the 
class SocketWrapper:
    def __init__(self, socket, socket_name):
        self.socket = socket
        self.socket_name = socket_name
        self.received_message_queue = Queue()
    
    def wait(self):
        received_message = self.socket.wait()
        self.received_message_queue.put(received_message)
        return received_message

    def get_message(self):
        return self.received_message_queue.get()
    
    def send_message(self, content):
        print(f"updating {self.socket_name} with {content}")
        self.socket.send(str(content))
    
    def connection_loop(self):
        while True:
            received_message = self.wait()
            # if the client closed the connection, break out
            if received_message == None:
                return