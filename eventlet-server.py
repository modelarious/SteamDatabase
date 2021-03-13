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
    def __init__(self):
        pass

    def track_game_socket(self, ws):
        self.game_socket = ws
    
    def send_to_game_socket(self, content):
        self.game_socket.send(str(content))

# def state_updates(ws):
#     arr = []
#     for i in range(10):
#         arr.append(i)
#         ws.send(str(arr))
#         print(ws.path)
#         from_browser = ws.wait()
#         print(from_browser)

@websocket.WebSocketWSGI
def socket_collector(ws):
    connectionStorage.track_game_socket(ws)

def server():
    # wsgi.server(eventlet.listen(('', 8090)), hello_world)
    wsgi.server(eventlet.listen(('', 8091)), socket_collector)

from multiprocessing import Process
from time import sleep
if __name__ == '__main__':
    connectionStorage = ConnectionStorage()
    serverProcess = Process(target=server)
    serverProcess.start()


    sleep(30)
    print("writing to socket")
    connectionStorage.send_to_game_socket('helllo')
    connectionStorage.send_to_game_socket('hi there')
    serverProcess.join()
