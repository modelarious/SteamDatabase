import pickle
from typing import List

class DirListFetcherMOCKDATA:
    def get_dirs(self, pathToGamesFolder: str) -> List[str]:
        print("mocking the local games list from directory")
        with open('mockGamesList.txt', 'rb') as mockGamesList:
            gamesOnDisk = pickle.load(mockGamesList)
        return gamesOnDisk
