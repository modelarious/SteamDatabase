// import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Switch, Route, Link } from "react-router-dom";
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
import GameListView from './Views/GameListView';
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

// class App extends Component {
//   constructor() {
//     super();
//     this.state = {};
//     for (const state of STATES.concat([GAMES])) {
//       this.state[state] = [];
//     }
//     this.socketContainer = socketContainer;
//     autoBind(this);
//   }
  
//   componentDidMount() {
//     const sockets = Object.entries(socketContainer.get_sockets())
//     for (const [state, sock] of sockets) {
//       sock.onmessage = (message) => {
//         const receivedMessage = JSON.parse(message.data);
//         this.setState({
//           [state]: receivedMessage
//         });
//       };

//       sock.onopen = () => {
//         console.log(`${state} open`);
//       };
//       sock.onclose = () => {
//         console.log(`${state} close`);
//       }
//     }
//   }
  
//   render() {
//     var debugBoardNeededStateData = {}
//     for (const stateName of STATES) {
//       debugBoardNeededStateData[stateName] = this.state[stateName];
//     }

//     let commandSocket;
//     if (this.socketContainer) {
//       commandSocket = this.socketContainer.get_socket(COMMAND)
//     }

//     return (
//       <Tabs renderActiveTabContentOnly={true}>
//         <TabLink to="tab1" default>Games</TabLink>
//         <TabLink to="tab2">User Input</TabLink>
//         <TabLink to="tab3">Debug</TabLink>
      
//         <TabContent for="tab1">
//           <GameListView games={this.state[GAMES]}></GameListView>
//         </TabContent>
//         <TabContent for="tab2">"user input view"</TabContent>
//         <TabContent for="tab3">
//           <DebugBoard stateData={debugBoardNeededStateData} commandSocket={commandSocket}/>
//         </TabContent>
//       </Tabs>
//     );
//   }
// }

function Links(props) {
  const games = Object.values(props.games)
  return games.map(game => (
    <Link to={`/games/${game.steam_id}`}>
      <img
        alt={`${game.game_name_on_steam} link`}
        src={game.banner_link}
      />
    </Link>
  ));
};

function Home(props) {
  const games = props.games;
  return <Links games={games}/>
};

// All route props (match, location and history) are available to GameView
function GameView(props) {
  console.log(props);
  return (
    <div>
      <Link to="/"> Back </Link>
      <h1>Steam ID: {props.match.params.steam_id}!</h1>
    </div>
  );
}

function App() {
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
                  <Route path="/games/:steam_id" component={GameView}>
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