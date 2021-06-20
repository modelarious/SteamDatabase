import pickle
class SteamGameListFetcherMOCKDATA:
    def fetch_games_list(self):
        print("mocking the steam games list from API")
        with open('mockSteamReturn.txt', 'rb') as mockSteamReturn:
            steamGamesList = pickle.load(mockSteamReturn)
        
        print(steamGamesList)
        # exit()

        return steamGamesList

