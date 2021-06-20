from dataclasses import dataclass
from typing import List, Optional

# XXX none of the logging stuff should be here
# XXX XXX XXX you should be injecting the logger
import logging

# https://stackoverflow.com/a/11233293/7520564 used this answer to help me figure out how to 
# set up multiple loggers with different output files
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
def create_logger(name, log_file):
	handler = logging.FileHandler(log_file)        
	handler.setFormatter(formatter)
	logger = logging.getLogger(name)
	logger.addHandler(handler)
	return logger

basic_logger = create_logger('basic', '/tmp/basic-out.txt')
extended_logger = create_logger('extended', '/tmp/extended-out.txt')

@dataclass
class ScreenshotURL:
	thumbnail_url: str
	fullsize_url: str

@dataclass
class AppDetail:
	detailed_description: str
	about_the_game: str
	short_description: str
	header_image_url: str
	developers: List[str]
	publishers: List[str]
	metacritic_score: int
	controller_support: bool
	genres: List[str]
	screenshot_urls: List[ScreenshotURL]
	background_image_url: str


# maps the response from appdetails endpoint to an AppDetail object
class AppDetailFactory:
	def create_app_detail(self, steam_response, app_id: int) -> AppDetail:
		# XXX HAS THIS BEEN MOVED INTO THE PARENT?
		try:
			app_detail_response = steam_response[app_id]['data']
		except KeyError as e:
			message = f"broke on this input: {steam_response}, {e}"
			logging.critical(message)
			raise KeyError(message)
		screenshot_urls = self._get_screenshot_urls(app_detail_response, app_id)
		genres = self._get_genres(app_detail_response, app_id)
		metacritic_score = self._get_metacritic_score(app_detail_response, app_id)
		controller_support = self._get_controller_support(app_detail_response, app_id)
		developers = self._get_developers(app_detail_response, app_id)
		return AppDetail(
			detailed_description=app_detail_response['detailed_description'],
			about_the_game=app_detail_response['about_the_game'],
			short_description=app_detail_response['short_description'],
			header_image_url=app_detail_response['header_image'],
			developers=developers,
			publishers=app_detail_response['publishers'],
			controller_support=controller_support,
			genres=genres,
			screenshot_urls=screenshot_urls,
			background_image_url=app_detail_response['background'],
			metacritic_score=metacritic_score
		)
	
	def _error_handling(self, app_detail_response, app_id, field_name):
		basic_log_message = f"{app_id} has no {field_name}. "
		basic_logger.error(basic_log_message)

		extended_message = f"{basic_log_message} Context={app_detail_response}"
		extended_logger.error(extended_message)
		# logging.error(extended_message)
	
	def _get_developers(self, app_detail_response, app_id):
		if 'developers' in app_detail_response:
			return app_detail_response['developers']
		self._error_handling(app_detail_response, app_id, 'developers')
		return []

	def _get_controller_support(self, app_detail_response, app_id) -> bool:
		if "controller_support" in app_detail_response:
			return True
		if "categories" in app_detail_response:
			for category_object in app_detail_response["categories"]:
				if 'controller' in category_object['description']:
					return True        
		return False

	def _get_screenshot_urls(self, app_detail_response, app_id) -> List[ScreenshotURL]:
		field_name = 'screenshots'
		screenshot_urls = []
		if field_name not in app_detail_response:
			self._error_handling(app_detail_response, app_id, field_name)
			return screenshot_urls

		for screenshot_object in app_detail_response[field_name]:
			screenshot_url = ScreenshotURL(
				thumbnail_url=screenshot_object['path_thumbnail'], 
				fullsize_url=screenshot_object['path_full']
			)
			screenshot_urls.append(screenshot_url)
		return screenshot_urls
	
	def _get_genres(self, app_detail_response, app_id) -> List[str]:
		field_name = 'genres'
		genres = []
		if field_name not in app_detail_response:
			self._error_handling(app_detail_response, app_id, field_name)
			return genres

		for genre_object in app_detail_response[field_name]:
			genres.append(genre_object['description'])
		return genres
	
	def _get_metacritic_score(self, app_detail_response, app_id) -> Optional[int]:            
		if 'metacritic' in app_detail_response:
			if 'score' in app_detail_response['metacritic']:
				return app_detail_response['metacritic']['score']
		self._error_handling(app_detail_response, app_id, 'metacritic->score')
		return None

# {
#    "427520":{
#       "success":true,
#       "data":{
#          "type":"game",
#          "name":"Factorio",
#          "steam_appid":427520,
#          "required_age":0,
#          "is_free":false,
#          "dlc":[
#             436090
#          ],
# *         "detailed_description":"<strong>Factorio<\/strong> is a game in which you build and maintain factories. You will be mining resources, researching technologies, building infrastructure, automating production and fighting enemies. In the beginning you will find yourself chopping trees, mining ores and crafting mechanical arms and transport belts by hand, but in short time you can become an industrial powerhouse, with huge solar fields, oil refining and cracking, manufacture and deployment of construction and logistic robots, all for your resource needs. However this heavy exploitation of the planet's resources does not sit nicely with the locals, so you will have to be prepared to defend yourself and your machine empire. <br><br>Join forces with other players in cooperative <strong>Multiplayer<\/strong>, create huge factories, collaborate and delegate tasks between you and your friends. Add mods to increase your enjoyment, from small tweak and helper mods to complete game overhauls, Factorio's ground-up <strong>Modding support<\/strong> has allowed content creators from around the world to design interesting and innovative features. While the core gameplay is in the form of the freeplay scenario, there are a range of interesting challenges in the form of <strong>Scenarios<\/strong>. If you don't find any maps or scenarios you enjoy, you can create your own with the in-game <strong>Map Editor<\/strong>, place down entities, enemies, and terrain in any way you like, and even add your own custom script to make for interesting gameplay.<br><br><strong>Discount Disclaimer:<\/strong> We don't have any plans to take part in a sale or to reduce the price for the foreseeable future.<h2 class=\"bb_tag\">What people say about Factorio<\/h2><br><ul class=\"bb_ul\"><li><i>No other game in the history of gaming handles the logistics side of management simulator so perfectly.<\/i> - <strong>Reddit<\/strong><br><\/li><li><i>I see conveyor belts when I close my eyes. I may have been binging Factorio lately.<\/i> - <strong>Notch, Mojang<\/strong><br><\/li><li><i>Factorio is a super duper awesome game where we use conveyor belts to shoot aliens.<\/i> - <strong>Zisteau, Youtube<\/strong><\/li><\/ul>",
# *         "about_the_game":"<strong>Factorio<\/strong> is a game in which you build and maintain factories. You will be mining resources, researching technologies, building infrastructure, automating production and fighting enemies. In the beginning you will find yourself chopping trees, mining ores and crafting mechanical arms and transport belts by hand, but in short time you can become an industrial powerhouse, with huge solar fields, oil refining and cracking, manufacture and deployment of construction and logistic robots, all for your resource needs. However this heavy exploitation of the planet's resources does not sit nicely with the locals, so you will have to be prepared to defend yourself and your machine empire. <br><br>Join forces with other players in cooperative <strong>Multiplayer<\/strong>, create huge factories, collaborate and delegate tasks between you and your friends. Add mods to increase your enjoyment, from small tweak and helper mods to complete game overhauls, Factorio's ground-up <strong>Modding support<\/strong> has allowed content creators from around the world to design interesting and innovative features. While the core gameplay is in the form of the freeplay scenario, there are a range of interesting challenges in the form of <strong>Scenarios<\/strong>. If you don't find any maps or scenarios you enjoy, you can create your own with the in-game <strong>Map Editor<\/strong>, place down entities, enemies, and terrain in any way you like, and even add your own custom script to make for interesting gameplay.<br><br><strong>Discount Disclaimer:<\/strong> We don't have any plans to take part in a sale or to reduce the price for the foreseeable future.<h2 class=\"bb_tag\">What people say about Factorio<\/h2><br><ul class=\"bb_ul\"><li><i>No other game in the history of gaming handles the logistics side of management simulator so perfectly.<\/i> - <strong>Reddit<\/strong><br><\/li><li><i>I see conveyor belts when I close my eyes. I may have been binging Factorio lately.<\/i> - <strong>Notch, Mojang<\/strong><br><\/li><li><i>Factorio is a super duper awesome game where we use conveyor belts to shoot aliens.<\/i> - <strong>Zisteau, Youtube<\/strong><\/li><\/ul>",
# *         "short_description":"Factorio is a game about building and creating automated factories to produce items of increasing complexity, within an infinite 2D world. Use your imagination to design your factory, combine simple elements into ingenious structures, and finally protect it from the creatures who don't really like you.",
#          "supported_languages":"English, French, Italian, German, Spanish - Spain, Hungarian, Dutch, Norwegian, Polish, Portuguese, Portuguese - Brazil, Romanian, Finnish, Swedish, Czech, Russian, Ukrainian, Japanese, Simplified Chinese, Traditional Chinese, Korean, Turkish",
# *         "header_image":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/header.jpg?t=1620730652",
#          "website":"https:\/\/www.factorio.com",
#          "pc_requirements":{
#             "minimum":"<strong>Minimum:<\/strong><br><ul class=\"bb_ul\"><li><strong>OS:<\/strong> Windows 10, 8, 7, Vista (64 Bit)<br><\/li><li><strong>Processor:<\/strong> Dual core 3Ghz+<br><\/li><li><strong>Memory:<\/strong> 4 GB RAM<br><\/li><li><strong>Graphics:<\/strong> DirectX 10.1 capable GPU with 512 MB VRAM - GeForce GTX 260, Radeon HD 4850 or Intel HD Graphics 5500<br><\/li><li><strong>DirectX:<\/strong> Version 11<br><\/li><li><strong>Storage:<\/strong> 3 GB available space<br><\/li><li><strong>Additional Notes:<\/strong> Normal sprite resolution, Low quality compression, 1080p resolution<\/li><\/ul>",
#             "recommended":"<strong>Recommended:<\/strong><br><ul class=\"bb_ul\"><li><strong>OS:<\/strong> Windows 10, 8, 7 (64 Bit)<br><\/li><li><strong>Processor:<\/strong> Quad core 3Ghz+<br><\/li><li><strong>Memory:<\/strong> 8 GB RAM<br><\/li><li><strong>Graphics:<\/strong> DirectX 11 capable GPU with 2 GB VRAM - GeForce GTX 750 Ti, Radeon R7 360<br><\/li><li><strong>DirectX:<\/strong> Version 11<br><\/li><li><strong>Storage:<\/strong> 3 GB available space<br><\/li><li><strong>Additional Notes:<\/strong> High sprite resolution, High quality compression<\/li><\/ul>"
#          },
#          "mac_requirements":{
#             "minimum":"<strong>Minimum:<\/strong><br><ul class=\"bb_ul\"><li><strong>OS:<\/strong> macOS Catalina, Mojave, High Sierra, Sierra, OSX El Capitan, Yosemite<br><\/li><li><strong>Processor:<\/strong> Dual core 3Ghz+<br><\/li><li><strong>Memory:<\/strong> 4 GB RAM<br><\/li><li><strong>Graphics:<\/strong> 2012 Mac<br><\/li><li><strong>Storage:<\/strong> 3 GB available space<br><\/li><li><strong>Additional Notes:<\/strong> Normal sprite resolution, Low quality compression, 1080p resolution<\/li><\/ul>",
#             "recommended":"<strong>Recommended:<\/strong><br><ul class=\"bb_ul\"><li><strong>OS:<\/strong> macOS Catalina, Mojave, High Sierra, Sierra, OSX El Capitan, Yosemite<br><\/li><li><strong>Processor:<\/strong> Quad core 3GHz+<br><\/li><li><strong>Memory:<\/strong> 8 GB RAM<br><\/li><li><strong>Graphics:<\/strong> 2015 Mac with dedicated GPU with 2 GB VRAM.<br><\/li><li><strong>Storage:<\/strong> 3 GB available space<br><\/li><li><strong>Additional Notes:<\/strong> High sprite resolution, High quality compression<\/li><\/ul>"
#          },
#          "linux_requirements":{
#             "minimum":"<strong>Minimum:<\/strong><br><ul class=\"bb_ul\"><li><strong>OS:<\/strong> Linux (tarball installation)<br><\/li><li><strong>Processor:<\/strong> Dual core 3Ghz+<br><\/li><li><strong>Memory:<\/strong> 4 GB RAM<br><\/li><li><strong>Graphics:<\/strong> OpenGL 3.3 core, DirectX 10.1 capable GPU with 512 MB VRAM - GeForce GTX 260, Radeon HD 4850 or Intel HD Graphics 5500<br><\/li><li><strong>Storage:<\/strong> 3 GB available space<br><\/li><li><strong>Sound Card:<\/strong> PulseAudio<br><\/li><li><strong>Additional Notes:<\/strong> Normal sprite resolution, Low quality compression, 1080p resolution<\/li><\/ul>",
#             "recommended":"<strong>Recommended:<\/strong><br><ul class=\"bb_ul\"><li><strong>OS:<\/strong> Linux (tarball installation)<br><\/li><li><strong>Processor:<\/strong> Quad core 3GHz+<br><\/li><li><strong>Memory:<\/strong> 8 GB RAM<br><\/li><li><strong>Graphics:<\/strong> OpenGL 4.3 core, DirectX 11 capable GPU with 2 GB VRAM - GeForce GTX 750 Ti, Radeon R7 360<br><\/li><li><strong>Storage:<\/strong> 3 GB available space<br><\/li><li><strong>Sound Card:<\/strong> PulseAudio<br><\/li><li><strong>Additional Notes:<\/strong> High sprite resolution, High quality compression<\/li><\/ul>"
#          },
#          "legal_notice":"All rights reserved",
# *         "developers":[
#             "Wube Software LTD."
#          ],
# *         "publishers":[
#             "Wube Software LTD."
#          ],
#          "demos":[
#             {
#                "appid":452280,
#                "description":"Factorio Demo"
#             }
#          ],
#          "price_overview":{
#             "currency":"CAD",
#             "initial":3400,
#             "final":3400,
#             "discount_percent":0,
#             "initial_formatted":"",
#             "final_formatted":"CDN$ 34.00"
#          },
#          "packages":[
#             88199
#          ],
#          "package_groups":[
#             {
#                "name":"default",
#                "title":"Buy Factorio",
#                "description":"",
#                "selection_text":"Select a purchase option",
#                "save_text":"",
#                "display_type":0,
#                "is_recurring_subscription":"false",
#                "subs":[
#                   {
#                      "packageid":88199,
#                      "percent_savings_text":" ",
#                      "percent_savings":0,
#                      "option_text":"Factorio - CDN$ 34.00",
#                      "option_description":"",
#                      "can_get_free_license":"0",
#                      "is_free_license":false,
#                      "price_in_cents_with_discount":3400
#                   }
#                ]
#             }
#          ],
#          "platforms":{
#             "windows":true,
#             "mac":true,
#             "linux":true
#          },
#          "metacritic":{
# *            "score":91,
#             "url":"https:\/\/www.metacritic.com\/game\/pc\/factorio?ftag=MCD-06-10aaa1f"
#          },
# * controller support?
#          "categories":[
#             {
#                "id":2,
#                "description":"Single-player"
#             },
#             {
#                "id":1,
#                "description":"Multi-player"
#             },
#             {
#                "id":9,
#                "description":"Co-op"
#             },
#             {
#                "id":38,
#                "description":"Online Co-op"
#             },
#             {
#                "id":48,
#                "description":"LAN Co-op"
#             },
#             {
#                "id":27,
#                "description":"Cross-Platform Multiplayer"
#             },
#             {
#                "id":22,
#                "description":"Steam Achievements"
#             },
#             {
#                "id":23,
#                "description":"Steam Cloud"
#             },
#             {
#                "id":17,
#                "description":"Includes level editor"
#             },
#             {
#                "id":42,
#                "description":"Remote Play on Tablet"
#             }
#          ],
# *         "genres":[
#             {
#                "id":"4",
#                "description":"Casual"
#             },
#             {
#                "id":"23",
#                "description":"Indie"
#             },
#             {
#                "id":"28",
#                "description":"Simulation"
#             },
#             {
#                "id":"2",
#                "description":"Strategy"
#             }
#          ],
# *         "screenshots":[
#             {
#                "id":0,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_36e4d8e5540805f5ed492d24d784ed9ba661752b.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_36e4d8e5540805f5ed492d24d784ed9ba661752b.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":1,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_171f398a8e347fad650a9c1b6c3b77c612781510.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_171f398a8e347fad650a9c1b6c3b77c612781510.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":2,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_0bf814493f247b6baa093511b46c352cf9e98435.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_0bf814493f247b6baa093511b46c352cf9e98435.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":3,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_2533e54b0bd90a29adbedb60108ed277536ad445.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_2533e54b0bd90a29adbedb60108ed277536ad445.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":4,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_192864c00fc38b5ef97b97ca7fa655a9aed7c0da.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_192864c00fc38b5ef97b97ca7fa655a9aed7c0da.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":5,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_e301bde0fc0e996ba93e92639cd49dd90ae47b36.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_e301bde0fc0e996ba93e92639cd49dd90ae47b36.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":6,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_57665be6cc629906ae7004799e90699c69c07c97.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_57665be6cc629906ae7004799e90699c69c07c97.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":7,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_9dba6c91d45eededca01f9f61bf1435be2dfbf0d.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_9dba6c91d45eededca01f9f61bf1435be2dfbf0d.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":8,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_124dc8dc3fd282f6feb2d9ee20aebd2d73188e02.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_124dc8dc3fd282f6feb2d9ee20aebd2d73188e02.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":9,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_2c4dcb9195a91014ce1189707af3127c4db9b2b0.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_2c4dcb9195a91014ce1189707af3127c4db9b2b0.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":10,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_5903f8ff243e9a89b4f1e15e6e7982159578f8ec.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_5903f8ff243e9a89b4f1e15e6e7982159578f8ec.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":11,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_0e6d3c0d1af06fcde28ef1f1703e142f416ace44.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_0e6d3c0d1af06fcde28ef1f1703e142f416ace44.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":12,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_aee9573a97f97fbb7daac6c76709c62228ec5e00.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_aee9573a97f97fbb7daac6c76709c62228ec5e00.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":13,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_b3cbbdb8e10d2f172297c4cc792d908fdb68529e.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_b3cbbdb8e10d2f172297c4cc792d908fdb68529e.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":14,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_caac427e023e8682cc4bf1aba233538cf267e6fa.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_caac427e023e8682cc4bf1aba233538cf267e6fa.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":15,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_0714db2482893b77d8622604eaf9d3788734c7a6.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_0714db2482893b77d8622604eaf9d3788734c7a6.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":16,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_3f93f2655cbc3db0da1b3e888aa68a8a9f5f6a47.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_3f93f2655cbc3db0da1b3e888aa68a8a9f5f6a47.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":17,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_0a6e8dbaa59e8fa5327d4fd2c8bb2a6909dc864c.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_0a6e8dbaa59e8fa5327d4fd2c8bb2a6909dc864c.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":18,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_46b600e169426189343f525860cb705fecbbc3db.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_46b600e169426189343f525860cb705fecbbc3db.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":19,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_707a4120fed96e579f56d350ae076c20e205ae8f.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_707a4120fed96e579f56d350ae076c20e205ae8f.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":20,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_88545f5f01c635ea0001f3849f064f058dbdf81d.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_88545f5f01c635ea0001f3849f064f058dbdf81d.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":21,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_0a6343acf3b3a3d2b1d23e3bc4a21cb890ec14b8.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_0a6343acf3b3a3d2b1d23e3bc4a21cb890ec14b8.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":22,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_4a8af525907d5711cee45f9df4f55565484fb409.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_4a8af525907d5711cee45f9df4f55565484fb409.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":23,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_75c02d35dcecc57a747e7a9ec9df4806ef8b3be2.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_75c02d35dcecc57a747e7a9ec9df4806ef8b3be2.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":24,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_37aa19e26e20e18a220fd8870dac6efb0e98b5f0.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_37aa19e26e20e18a220fd8870dac6efb0e98b5f0.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":25,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_b9a77ea7a73d9acf22d6e86215d7376cdcd0eb9c.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_b9a77ea7a73d9acf22d6e86215d7376cdcd0eb9c.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":26,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_5b4ca37921ff8a0b9ad328028179d3d3a952f1a4.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_5b4ca37921ff8a0b9ad328028179d3d3a952f1a4.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":27,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_a849d4a6b7d990ad6669906be9d8de44c4fb2ef2.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_a849d4a6b7d990ad6669906be9d8de44c4fb2ef2.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":28,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_6418c33bc4ce393557507089ba28fc5220e2b8e0.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_6418c33bc4ce393557507089ba28fc5220e2b8e0.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":29,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_a066c38bbd26f5b5e8b0385e6e84efc4de4aceed.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_a066c38bbd26f5b5e8b0385e6e84efc4de4aceed.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":30,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_00c51f1518de5ff75ef884cf3f66ee50e4e5ded1.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_00c51f1518de5ff75ef884cf3f66ee50e4e5ded1.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":31,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_21820439ab772913e4be55ec2db5165eac655e8c.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_21820439ab772913e4be55ec2db5165eac655e8c.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":32,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_773b26c58fede6b7e6df879d1d3a73f840f72114.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_773b26c58fede6b7e6df879d1d3a73f840f72114.1920x1080.jpg?t=1620730652"
#             },
#             {
#                "id":33,
#                "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_3e68dabdf5c6f465d7ec891beba137c8f7e31f78.600x338.jpg?t=1620730652",
#                "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/ss_3e68dabdf5c6f465d7ec891beba137c8f7e31f78.1920x1080.jpg?t=1620730652"
#             }
#          ],
#          "movies":[
#             {
#                "id":256796273,
#                "name":"Teaser 2020",
#                "thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256796273\/movie.293x165.jpg?t=1597395499",
#                "webm":{
#                   "480":"http:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256796273\/movie480_vp9.webm?t=1597395499",
#                   "max":"http:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256796273\/movie_max_vp9.webm?t=1597395499"
#                },
#                "mp4":{
#                   "480":"http:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256796273\/movie480.mp4?t=1597395499",
#                   "max":"http:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256796273\/movie_max.mp4?t=1597395499"
#                },
#                "highlight":true
#             },
#             {
#                "id":256660593,
#                "name":"Gameplay Trailer",
#                "thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256660593\/movie.293x165.jpg?t=1456427081",
#                "webm":{
#                   "480":"http:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256660593\/movie480.webm?t=1456427081",
#                   "max":"http:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256660593\/movie_max.webm?t=1456427081"
#                },
#                "mp4":{
#                   "480":"http:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256660593\/movie480.mp4?t=1456427081",
#                   "max":"http:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256660593\/movie_max.mp4?t=1456427081"
#                },
#                "highlight":true
#             },
#             {
#                "id":256796265,
#                "name":"1.0 launch trailer",
#                "thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256796265\/movie.293x165.jpg?t=1597395492",
#                "webm":{
#                   "480":"http:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256796265\/movie480_vp9.webm?t=1597395492",
#                   "max":"http:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256796265\/movie_max_vp9.webm?t=1597395492"
#                },
#                "mp4":{
#                   "480":"http:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256796265\/movie480.mp4?t=1597395492",
#                   "max":"http:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/256796265\/movie_max.mp4?t=1597395492"
#                },
#                "highlight":false
#             }
#          ],
#          "recommendations":{
#             "total":93795
#          },
#          "achievements":{
#             "total":38,
#             "highlighted":[
#                {
#                   "name":"Automated cleanup",
#                   "path":"https:\/\/cdn.akamai.steamstatic.com\/steamcommunity\/public\/images\/apps\/427520\/faee0ff18317271e413623fe5d51ab4660448f0f.jpg"
#                },
#                {
#                   "name":"Automated construction",
#                   "path":"https:\/\/cdn.akamai.steamstatic.com\/steamcommunity\/public\/images\/apps\/427520\/94b991a87d1c3daf3c91f9294f337ae68f7e112d.jpg"
#                },
#                {
#                   "name":"Circuit veteran 1",
#                   "path":"https:\/\/cdn.akamai.steamstatic.com\/steamcommunity\/public\/images\/apps\/427520\/545caae09a11e1d2781d034c5e82b2cb517adcfb.jpg"
#                },
#                {
#                   "name":"Circuit veteran 2",
#                   "path":"https:\/\/cdn.akamai.steamstatic.com\/steamcommunity\/public\/images\/apps\/427520\/fd8982a6b9ada7ea85536c869ad78bf690330e4c.jpg"
#                },
#                {
#                   "name":"Circuit veteran 3",
#                   "path":"https:\/\/cdn.akamai.steamstatic.com\/steamcommunity\/public\/images\/apps\/427520\/977c7ae92d2d5293aceb718260651571044c1113.jpg"
#                },
#                {
#                   "name":"Computer age 1",
#                   "path":"https:\/\/cdn.akamai.steamstatic.com\/steamcommunity\/public\/images\/apps\/427520\/718bb88092dbf7f5208f296754ab77118874935a.jpg"
#                },
#                {
#                   "name":"Computer age 2",
#                   "path":"https:\/\/cdn.akamai.steamstatic.com\/steamcommunity\/public\/images\/apps\/427520\/4842d765a15cc41bf63b61d7c0d8ff782ae324f0.jpg"
#                },
#                {
#                   "name":"Computer age 3",
#                   "path":"https:\/\/cdn.akamai.steamstatic.com\/steamcommunity\/public\/images\/apps\/427520\/10e730acf6c5fe42f414c004d84695f6f4d14099.jpg"
#                },
#                {
#                   "name":"You've got a package",
#                   "path":"https:\/\/cdn.akamai.steamstatic.com\/steamcommunity\/public\/images\/apps\/427520\/1f1528f292a3820e5b5971c680efc50ad20e8320.jpg"
#                },
#                {
#                   "name":"Delivery service",
#                   "path":"https:\/\/cdn.akamai.steamstatic.com\/steamcommunity\/public\/images\/apps\/427520\/39ca8823f562502d3bd1e4b5c7f43fb19ab41cbb.jpg"
#                }
#             ]
#          },
#          "release_date":{
#             "coming_soon":false,
#             "date":"14 Aug, 2020"
#          },
#          "support_info":{
#             "url":"http:\/\/www.factorio.com\/support-overview",
#             "email":"support@factorio.com"
#          },
# *         "background":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/427520\/page_bg_generated_v6b.jpg?t=1620730652",
#          "content_descriptors":{
#             "ids":[
			   
#             ],
#             "notes":null
#          }
#       }
#    }
# }