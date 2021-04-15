import pickle

class DirListFetcherMOCKDATA:
    def get_dirs(self, pathToGamesFolder: str):
        print("mocking the local games list from directory")
        with open('mockGamesList.txt', 'rb') as mockGamesList:
            gamesOnDisk = pickle.load(mockGamesList)
        return gamesOnDisk
