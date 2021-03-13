"""This is a simple example of running a wsgi application with eventlet.
For a more fully-featured server which supports multiple processes,
multiple threads, and graceful code reloading, see:

http://pypi.python.org/pypi/Spawning/
"""

# import eventlet
# from eventlet import wsgi


# def hello_world(env, start_response):
#     if env['PATH_INFO'] != '/':
#         start_response('404 Not Found', [('Content-Type', 'text/plain')])
#         return ['Not Found\r\n']
#     start_response('200 OK', [('Content-Type', 'text/plain')])
#     return ['Hello, World!\r\n']

# wsgi.server(eventlet.listen(('', 5001)), hello_world)


from eventlet import wsgi, websocket
import eventlet

@websocket.WebSocketWSGI
def hello_world(ws):
    while True:
        ws.send("hello world")
        from_browser = ws.wait()
        print(from_browser)

class ConnectionStorage:
    def track_game_socket(self, ws):
        self.game_socket = ws
        #XXX this is dangling - should this be returned and waited on in the main process?
        #XXX Essentially you are read blocking on this socket - you can still write to it
        #XXX from other threads, but you can't join the thread that's read blocked.  You also
        #XXX can't guarantee that the clients will close the connections
        #
        #XXX actually - it looks like when a client disconnects, these will all unblock
        self.game_socket.wait() 
    
    def send_to_game_socket(self, content):
        print(f"updating game_socket with content {content}")
        print(self.game_socket)
        self.game_socket.send(str(content))
    
    def track_no_socket(self, ws):
        self.no_socket = ws

        self.no_socket.wait() 
    
    def send_to_no_socket(self, content):
        print(f"updating no_socket with content {content}")
        print(self.no_socket)
        self.no_socket.send(str(content))


# def state_updates(ws):
#     arr = []
#     for i in range(10):
#         arr.append(i)
#         ws.send(str(arr))
#         print(ws.path)
#         from_browser = ws.wait()
#         print(from_browser)




# def server():
#     pass


from threading import Thread
from time import sleep
if __name__ == '__main__':
    connectionStorage = ConnectionStorage()

    def server(connectionStorage):
        # wsgi.server(eventlet.listen(('', 8090)), hello_world)
        @websocket.WebSocketWSGI
        def socket_collector(ws):
            print(ws.path)
            if ws.path == "/game":
                connectionStorage.track_game_socket(ws)
            elif ws.path == "/no":
                connectionStorage.track_no_socket(ws)
                
        wsgi.server(eventlet.listen(('', 8091)), socket_collector)

    serverThread = Thread(target=server, args = (connectionStorage,))
    serverThread.start()
    sleep(30)
    print("writing to sockets /no and /game")
    print(f"connectionStorage = {connectionStorage}")
    connectionStorage.send_to_game_socket('helllo')
    connectionStorage.send_to_game_socket('hi there')
    connectionStorage.send_to_no_socket('secret secret')
    serverThread.join()
