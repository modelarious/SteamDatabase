from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from Server.Server import Server
from StateTracker import StateTracker

if __name__ == '__main__':
    websocketClientHandlerRegistry = WebsocketClientHandlerRegistry()
    server = Server(websocketClientHandlerRegistry)
    server.startInThread()

    stateTracker = StateTracker(websocketClientHandlerRegistry)

    from time import sleep
    stateTracker.setUpcomingState('factorio')
    sleep(1)
    stateTracker.setUpcomingState('satisfactory')
    sleep(3)
    stateTracker.setFindingNameActiveState('factorio')
    sleep(3)
    stateTracker.setFindingNameActiveState('satisfactory')
    

    # XXX all below is driver code
    from json import dumps
    input("tell me when you're connected")

    GAME_SOCKET = '/game'

    gameSock = websocketClientHandlerRegistry.get_socket(GAME_SOCKET)

    jsonMessage = dumps({
        "games" : [
            { 'steamID': 3, 'steamName': 'game 3' },
            { 'steamID': 4, 'steamName': 'game 4' }
        ]
    })
    gameSock.send_message(jsonMessage)

    jsonMessage = dumps({
        "games" : [
            { 'steamID': 5, 'steamName': 'game 5' }
        ]
    })
    gameSock.send_message(jsonMessage)

    # print(gameSock.get_message())
    
    print("waiting on server")
    server.join()
