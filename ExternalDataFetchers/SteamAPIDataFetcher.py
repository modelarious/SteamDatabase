from dataclasses import dataclass, field
from typing import List, Optional
from ExternalDataFetchers.AppDetail import AppDetailFactory, AppDetail
import requests

class NoResponseException(Exception):
    pass

class RequestUnsuccesfulException(Exception):
    pass

class IncorrectAppTypeException(Exception):
    pass

@dataclass
class SteamAPIDataFetcher:
    app_detail_factory: AppDetailFactory
    allowed_app_types: List = field(default_factory=lambda: ['game', 'dlc', 'demo'])
    
    def getAvgReviewScore(self, steam_id: int) -> int:
        URL = f"https://store.steampowered.com/appreviews/{steam_id}?json=1 "
        requestReturn = requests.get(url = URL) 
        gamesObject = requestReturn.json()
        reviewValues = gamesObject['query_summary']
        return reviewValues['review_score']
    
    def get_app_detail(self, steam_id: int) -> Optional[AppDetail]:
        URL = f"https://store.steampowered.com/api/appdetails?appids={steam_id}"
        request_return = requests.get(url = URL)
        steam_response = request_return.json()
        if not steam_response:
            raise NoResponseException(f"got None when fetching from {URL}")

        app_id = list(steam_response.keys())[0]
        success = steam_response[app_id]['success']
        if not success:
            raise RequestUnsuccesfulException(f"request returned False in the `success` field: {steam_response}")

        app_type = steam_response[app_id]['data']['type']
        if app_type not in self.allowed_app_types:
            raise IncorrectAppTypeException(f"app_type ({app_type}) was not part of allowed app types: {self.allowed_app_types}")

        app_detail = self.app_detail_factory.create_app_detail(steam_response, app_id)
        return app_detail

#---------------------------------------------------------------------------------------
# https://store.steampowered.com/appreviews/2028850?json=1  
# review
# https://store.steampowered.com/api/appdetails?appids=2028850 
# "2028850" -> "data" -> "detailed_description"
# "2028850" -> "data" -> "categories":[
#     {
#        "id":2,
#        "description":"Single-player"
#     },
#     {
#        "id":21,
#        "description":"Downloadable Content"
#     },
#     {
#        "id":22,
#        "description":"Steam Achievements"
#     },
#     {
#        "id":28,
#        "description":"Full controller support"
#     },
#     {
#        "id":23,
#        "description":"Steam Cloud"
#     }
#  ],
#  "genres":[
#     {
#        "id":"1",
#        "description":"Action"
#     }
#  ],
#  "screenshots":[
#     {
#        "id":0,
#        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_c6f3fbf3e9f4cb1777462150203a7174608dfcd9.600x338.jpg?t=1560961334",
#        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_c6f3fbf3e9f4cb1777462150203a7174608dfcd9.1920x1080.jpg?t=1560961334"
#     },
#     {
#        "id":1,
#        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_d45294620026ff41f7e6b8610c6d60e13645fbf3.600x338.jpg?t=1560961334",
#        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_d45294620026ff41f7e6b8610c6d60e13645fbf3.1920x1080.jpg?t=1560961334"
#     },
#     {
#        "id":2,
#        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_3a364ffdcd2c1eeb3957435c624fc7c383d8cb69.600x338.jpg?t=1560961334",
#        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_3a364ffdcd2c1eeb3957435c624fc7c383d8cb69.1920x1080.jpg?t=1560961334"
#     },
#     {
#        "id":3,
#        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_26e2d983948edfb911db3e0d2c3679900b4ef9fa.600x338.jpg?t=1560961334",
#        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_26e2d983948edfb911db3e0d2c3679900b4ef9fa.1920x1080.jpg?t=1560961334"
#     },
#     {
#        "id":4,
#        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_4616da02724c2beaa8afc74a501929d27a65542a.600x338.jpg?t=1560961334",
#        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_4616da02724c2beaa8afc74a501929d27a65542a.1920x1080.jpg?t=1560961334"
#     },
#     {
#        "id":5,
#        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_fd6f5de55332f6c3cd119a01a9e017e840765c0e.600x338.jpg?t=1560961334",
#        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_fd6f5de55332f6c3cd119a01a9e017e840765c0e.1920x1080.jpg?t=1560961334"
#     },
#     {
#        "id":6,
#        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_37f25110f8d76335ddbc29a381bc6961e209acf6.600x338.jpg?t=1560961334",
#        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_37f25110f8d76335ddbc29a381bc6961e209acf6.1920x1080.jpg?t=1560961334"
#     },
#     {
#        "id":7,
#        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_dc76723504ce89c1ed1f66fd468682ba76548c32.600x338.jpg?t=1560961334",
#        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_dc76723504ce89c1ed1f66fd468682ba76548c32.1920x1080.jpg?t=1560961334"
#     },
#     {
#        "id":8,
#        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_e98deaf0e334206b84c2462276aee98107fa20d0.600x338.jpg?t=1560961334",
#        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_e98deaf0e334206b84c2462276aee98107fa20d0.1920x1080.jpg?t=1560961334"
#     }
#  ],
#  "release_date":{
#     "coming_soon":false,
#     "date":"25 Jun, 2013"
#  },