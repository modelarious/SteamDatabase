// import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Switch, Route, Link, useParams } from "react-router-dom";
// import { PageTransition } from "@steveeeie/react-page-transition";
// import "./styles.css";
import React, { Component } from 'react';
import SocketContainer from "./SocketContainer.js";
import { STATES } from './States.js';
import {
  TabLink,
  Tabs,
  TabContent
} from 'react-tabs-redux';
import DebugBoard from './Views/DebugBoard';
// import GameListView from './Views/GameListView';
const autoBind = require('auto-bind');
const COMMAND = "/command";
const GAMES = "/games";
const endpoints = STATES.concat([
  COMMAND,
  GAMES
]);

// XXX I really don't like this being global - but it seems to be the only way to
// establish these connections before the first render call triggers
const socketContainer = new SocketContainer(endpoints);

class App extends Component {
  constructor() {
    super();
    this.state = {};
    for (const state of STATES.concat([GAMES])) {
      this.state[state] = [];
    }
    this.socketContainer = socketContainer;
    autoBind(this);
  }
  
  componentDidMount() {
    const sockets = Object.entries(socketContainer.get_sockets())
    for (const [state, sock] of sockets) {
      sock.onmessage = (message) => {
        const receivedMessage = JSON.parse(message.data);
        this.setState({
          [state]: receivedMessage
        });
      };

      sock.onopen = () => {
        console.log(`${state} open`);
      };
      sock.onclose = () => {
        console.log(`${state} close`);
      }
    }
  }
  
  render() {
    var debugBoardNeededStateData = {}
    for (const stateName of STATES) {
      debugBoardNeededStateData[stateName] = this.state[stateName];
    }

    let commandSocket;
    if (this.socketContainer) {
      commandSocket = this.socketContainer.get_socket(COMMAND)
    }


    return (
      <Tabs renderActiveTabContentOnly={true}>
        <TabLink to="tab1" default>Games</TabLink>
        <TabLink to="tab2">User Input</TabLink>
        <TabLink to="tab3">Debug</TabLink>
      
        <TabContent for="tab1">
          <GameListViewBETTER games={this.state[GAMES]}></GameListViewBETTER>
        </TabContent>
        <TabContent for="tab2">"user input view"</TabContent>
        <TabContent for="tab3">
          <DebugBoard stateData={debugBoardNeededStateData} commandSocket={commandSocket}/>
        </TabContent>
      </Tabs>
    );
  }
}

function Links(props) {
  return props.games.map(game => (
    <Link to={`/games/${game.steam_id}`}>
      <img
        alt={`${game.game_name_on_steam} link`}
        src={game.app_detail.header_image_url}
      />
    </Link>
  ));
};

function Home(props) {
  const games = props.games;
  return <Links games={games}/>
};

function linear_search_by_steam_id(array_of_games, steam_id_to_find) {
  for (const game of array_of_games) {
    if (game.steam_id == steam_id_to_find) {
      return game;
    }
  }
}

function GameView(props) {
  let { steam_id } = useParams();
  const game = linear_search_by_steam_id(props.games, steam_id);
  return (
    <div>
      <Link to="/"> Back </Link>
      <h1>Steam ID: {game.steam_id}!</h1>
      <h1>Name: {game.game_name_on_disk}!</h1>
    </div>
  );
}

function GameListViewBETTER(props) {
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
  const games = props.games
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
                    <Home games={games}/>
                  </Route>
                  <Route path="/games/:steam_id">
                    <GameView games={games}/>
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

ReactDOM.render(<App />, document.getElementById("root"));

export default App;