import { useParams, Link } from "react-router-dom";
import Gallery from 'react-grid-gallery';
function linear_search_by_steam_id(array_of_games, steam_id_to_find) {
  for (const game of array_of_games) {
    // don't like using ==, but one source provides string and other provides int so this weak comparison is what I want
    // eslint-disable-next-line eqeqeq
    if (game.steam_id == steam_id_to_find) {
      return game;
    }
  }
}
/*
class Game(SteamSendable):
    // game_name_on_disk: str
    // game_name_from_steam: str
    // steam_id: int
    // path_on_harddrive: str
    // avg_review_score: int
    // user_defined_genres: List[str]
    // app_detail : AppDetail

class ScreenshotURL:
	// thumbnail_url: str
	// fullsize_url: str

class AppDetail:
	// detailed_description: str
	about_the_game: str
	short_description: str
	// header_image_url: str
	// developers: List[str]
	// publishers: List[str]
	// metacritic_score: int
	// controller_support: bool
	// genres: List[str]
	// screenshot_urls: List[ScreenshotURL]
	// background_image_url: str
*/
function GameView(props) {
  let { steam_id } = useParams();
  const game = linear_search_by_steam_id(props.games, steam_id);
  const app_detail = game.app_detail;
  
  const screenshots = app_detail.screenshot_urls.map(screenshot_obj =>
    ({
      src: screenshot_obj.fullsize_url,
      thumbnail: screenshot_obj.thumbnail_url,
      thumbnailWidth: 460,
      thumbnailHeight: 215,
    })
  );
  const genres = app_detail.genres.map((genre) =>
    <li>{genre}</li>
  );
  const user_defined_genres = game.user_defined_genres.map((genre) =>
    <li>{genre}</li>
  );
  const publishers = app_detail.publishers.map((publisher) =>
    <li>{publisher}</li>
  );
  const developers = app_detail.developers.map((developer) =>
    <li>{developer}</li>
  );
  return (
    <div style={{
        backgroundImage: `url(${app_detail.background_image_url})`,
        backgroundRepeat: 'no-repeat',
        backgroundColor: "#1c2838"
    }}>
      <Link to="/" style={{backgroundColor: "white"}}> Back </Link>
      <font style={{color: "white"}}>
        <h1>{game.game_name_from_steam}</h1>
        <h1>Avg review score: {game.avg_review_score}</h1>
        <div dangerouslySetInnerHTML={{ __html: app_detail.detailed_description }} />
        <div>
          <Gallery images={screenshots} enableImageSelection={false}/>
        </div>
        <h1>Steam ID: {game.steam_id}!</h1>
        {app_detail.controller_support && <h1>Controller support: Yes!</h1>}
        {app_detail.metacritic_score && <h1>Metacritic score: {app_detail.metacritic_score}</h1>}
        <h1>Path: {game.path_on_harddrive}</h1>
        <h1>Genres:</h1>
        <ul>{genres}</ul>
        <h1>Steam User Defined Genres:</h1>
        <ul>{user_defined_genres}</ul>
        <h1>Publishers:</h1>
        <ul>{publishers}</ul>
        <h1>Developers:</h1>
        <ul>{developers}</ul>

      </font>
    </div>
  );
}

export default GameView;