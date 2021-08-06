import { useParams, Link } from "react-router-dom";
function linear_search_by_steam_id(array_of_games, steam_id_to_find) {
  for (const game of array_of_games) {
    // don't like using ==, but one source provides string and other provides int so this weak comparison is what I want
    // eslint-disable-next-line eqeqeq
    if (game.steam_id == steam_id_to_find) {
      return game;
    }
  }
}

function GameView(props) {
  let { steam_id } = useParams();
  const game = linear_search_by_steam_id(props.games, steam_id);
  return (
    <div style={{backgroundColor: "#1c2838"}}>
      <Link to="/" style={{backgroundColor: "white"}}> Back </Link>
      <font style={{color: "white"}}>
        <h1>Steam ID: {game.steam_id}!</h1>
        <h1>Name on disk: {game.game_name_on_disk}!</h1>
      </font>
    </div>
  );
}

export default GameView;