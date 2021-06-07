from requests import get
from bs4 import BeautifulSoup as Soup

class UserDefinedGenresFetcher:
    def getGenres(self, steamID):
        steamPage = get(f"https://store.steampowered.com/app/{steamID}").content
        soup = Soup(steamPage, features="html.parser")

        userDefinedGenres = soup.select('.popular_tags > a')

        sanitizedUserDefinedGenres = []
        for genreNum in range(len(userDefinedGenres)):
            genreText = userDefinedGenres[genreNum].text.strip()
            sanitizedUserDefinedGenres.append(genreText)
        
        return sanitizedUserDefinedGenres