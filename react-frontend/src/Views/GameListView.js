import React from "react";
import { BrowserRouter, Switch, Route, Link } from "react-router-dom";
import GameView from "./GameView";
// import { PageTransition } from "@steveeeie/react-page-transition";


function Links(props) {
  return props.games.map((game) => (
    <Link to={`/games/${game.steam_id}`}>
      <img
        alt={`${game.game_name_on_steam} link`}
        src={game.app_detail.header_image_url}
      />
    </Link>
  ));
}

function Home(props) {
  const games = props.games;
  return <Links games={games} />;
}


function GameListView(props) {
  // const games = [
  //   {
  //     "steam_id" : 12345,
  //     "game_name_on_disk" : "Cities XXL",
  //     "app_detail" : {
  //       "header_image_url": "https://cdn.akamai.steamstatic.com/steam/apps/313010/header.jpg?t=1602859660",
  //     },
  //   },
  //   {
  //     "steam_id" : 135246,
  //     "game_name_on_disk" : "Factorio",
  //     "app_detail" : {
  //       "header_image_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/427520/header.jpg?t=1620730652",
  //     },
  //   }
  // ]
  const games = props.games;
  return (
    <React.StrictMode>
      <BrowserRouter>
        {/* Tabs go here and wrap the Route component - this is where I took Links from  */}
        <Route
          render={({ location }) => {
            return (
              // <PageTransition
              // transitionKey={location.pathname}
              // enterAnimation="moveFromTopFade"
              // exitAnimation="moveToBottomFade"
              // >
              <Switch location={location}>
                <Route exact path="/">
                  <Home games={games} />
                </Route>
                <Route path="/games/:steam_id">
                  <GameView games={games} />
                </Route>
              </Switch>
              // </PageTransition>
            );
          }}
        />
      </BrowserRouter>
    </React.StrictMode>
  );
}

export default GameListView;
