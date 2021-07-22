import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Switch, Route, Link } from "react-router-dom";
// import { PageTransition } from "@steveeeie/react-page-transition";
// import "./styles.css";
const games = {
  12345 : {
    "steam_id" : 12345,
    "name" : "Cities XXL",
    "banner_link" : "https://cdn.akamai.steamstatic.com/steam/apps/313010/header.jpg?t=1602859660",
    "more_stuff": "oh yeah"
  },
  135246 : {
    "steam_id" : 135246,
    "name" : "Factorio",
    "banner_link" : "https://cdn.cloudflare.steamstatic.com/steam/apps/427520/header.jpg?t=1620730652",
    "more_stuff": "happy days"
  }
}
function Links(games) {
  return Object.values(games).map(game => (
    <Link to={`/games/${game.steam_id}`}>
      <img
        alt={`${game.game_name_on_steam} link`}
        src={game.banner_link}
      />
    </Link>
  ));
};

const Home = () => (
  <div>
    <h1>Homee</h1>
    <Links />
  </div>
);

// All route props (match, location and history) are available to About
function GameView(props) {
  return (
    <div>
      <Link to="/"> Back </Link>
      <h1>Steam ID: {props.match.params.steam_id}!</h1>
    </div>
  );
}

function App() {
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
                  <Route exact path="/" component={Home} />
                  <Route path="/games/:steam_id" component={GameView} />
                </Switch>
              // </PageTransition>
            );
          }}
        />
      </BrowserRouter>
    </React.StrictMode>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));

export default App;