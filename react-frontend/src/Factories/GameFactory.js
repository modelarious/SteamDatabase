import AppDetail from "../Models/AppDetail";
import ScreenshotURL from "../Models/ScreenshotURL";
import Game from "../Models/Game";

export default class GameFactory {
  create_game(game_from_backend) {
    const app_detail_incoming = game_from_backend['app_detail'];
    const screenshot_urls_processed = app_detail_incoming['screenshot_urls'].map(
      screenshot_url_incoming => new ScreenshotURL(
        screenshot_url_incoming['thumbnail_url'],
        screenshot_url_incoming['fullsize_url']
      )
    );
    const app_detail_processed = new AppDetail(
      app_detail_incoming['detailed_description'],
      app_detail_incoming['about_the_game'],
      app_detail_incoming['short_description'],
      app_detail_incoming['header_image_url'],
      app_detail_incoming['developers'],
      app_detail_incoming['publishers'],
      app_detail_incoming['metacritic_score'],
      app_detail_incoming['controller_support'],
      app_detail_incoming['genres'],
      screenshot_urls_processed,
      app_detail_incoming['background_image_url']
    );
    return new Game(
      game_from_backend['game_name_on_disk'],
      game_from_backend['game_name_from_steam'],
      game_from_backend['steam_id'],
      game_from_backend['path_on_harddrive'],
      game_from_backend['avg_review_score'],
      game_from_backend['user_defined_genres'],
      app_detail_processed
    );
  }
}