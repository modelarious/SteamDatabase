/*
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
*/
export default class AppDetail {
    constructor(
      detailed_description,
      about_the_game,
      short_description,
      header_image_url,
      developers,
      publishers,
      metacritic_score,
      controller_support,
      genres,
      screenshot_urls,
      background_image_url) {
        this.detailed_description = detailed_description
        this.about_the_game = about_the_game
        this.short_description = short_description
        this.header_image_url = header_image_url
        this.developers = developers
        this.publishers = publishers
        this.metacritic_score = metacritic_score
        this.controller_support = controller_support
        this.genres = genres
        this.screenshot_urls = screenshot_urls
        this.background_image_url = background_image_url
    }
}