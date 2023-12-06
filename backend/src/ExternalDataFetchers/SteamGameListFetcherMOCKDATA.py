import pickle


class SteamGameListFetcherMOCKDATA:
    def fetch_games_list(self):
        print("mocking the steam games list from API")
        with open("MockData/mockSteamReturn.txt", "rb") as mockSteamReturn:
            steamGamesList = pickle.load(mockSteamReturn)

        return steamGamesList
