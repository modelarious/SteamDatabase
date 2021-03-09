from requests import get
from bs4 import BeautifulSoup as Soup

class UserDefinedTagsFetcher:
    def getTags(self, steamID):
        print(f"https://store.steampowered.com/app/{steamID}")
        # it will let you just put in id and it will fill it in for you
        steamPage = get(f"https://store.steampowered.com/app/{steamID}").content
        # steamPage = get('https://store.steampowered.com/app/427520/Factorio/').content
        soup = Soup(steamPage, features="html.parser")

        userDefinedTags = soup.select('.popular_tags > a')

        sanitizedUserDefinedTags = []
        for tagNum in range(len(userDefinedTags)):
            tagText = userDefinedTags[tagNum].text.strip()
            sanitizedUserDefinedTags.append(tagText)
        
        return sanitizedUserDefinedTags