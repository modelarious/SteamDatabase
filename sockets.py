from Server.ServerProxyObject import ServerProxyObject
from multiprocessing.managers import BaseManager

from multiprocessing import Lock, Manager

from SteamDatabase import match_steam_games_to_games_on_disk_and_store
from ExternalDataFetchers.SteamGameListFetcherMOCKDATA import SteamGameListFetcherMOCKDATA
from InternalDataFetchers.DirListFetcherMOCKDATA import DirListFetcherMOCKDATA

if __name__ == '__main__':
    class ShareObjectBetweenProcesses(BaseManager):  
        pass
  
    ShareObjectBetweenProcesses.register('ServerProxyObject', ServerProxyObject) 
    shareObjectBetweenProcesses = ShareObjectBetweenProcesses()  
    shareObjectBetweenProcesses.start()  
    serverProxyObject = shareObjectBetweenProcesses.ServerProxyObject()

    m = Manager()
    lock = m.Lock()

    # XXX this is shared with the cli - use abstract factory pattern to make mock data
    steamGameListFetcher = SteamGameListFetcherMOCKDATA()
    steamGamesList = steamGameListFetcher.fetch_games_list()

    dirListFetcher = DirListFetcherMOCKDATA()
    gamesOnDisk = dirListFetcher.get_dirs("")

    match_steam_games_to_games_on_disk_and_store(steamGamesList, gamesOnDisk, serverProxyObject, lock)

    m.join()
    shareObjectBetweenProcesses.join()
