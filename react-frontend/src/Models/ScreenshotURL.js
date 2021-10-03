/*
@dataclass
class ScreenshotURL:
	thumbnail_url: str
	fullsize_url: str
*/
export default class ScreenshotURL {
    constructor(
      thumbnail_url,
      fullsize_url) {
        this.thumbnail_url = thumbnail_url
        this.fullsize_url = fullsize_url
    }
}