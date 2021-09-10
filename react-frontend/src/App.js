import React, { Component } from 'react';
import SocketContainer from "./SocketContainer.js";
import { STATES } from './States.js';
import {
  TabLink,
  Tabs,
  TabContent
} from 'react-tabs-redux';
import GameFactory from "./Factories/GameFactory";
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

    const game_factory = new GameFactory()
    const games = this.state[GAMES].map(
      game_from_backend => game_factory.create_game(game_from_backend)
    );
    console.log(games)

    return (
      <Tabs renderActiveTabContentOnly={true}>
        <TabLink to="tab1" default>Games</TabLink>
        <TabLink to="tab2">User Input</TabLink>
        <TabLink to="tab3">Debug</TabLink>
      
        <TabContent for="tab1">
          <GameListView key={games} games={games} updateScrollDistance={this.scrollDistanceUpdate}></GameListView>
        </TabContent>
        <TabContent for="tab2">"user input view"</TabContent>
        <TabContent for="tab3">
          <DebugBoard stateData={debugBoardNeededStateData} commandSocket={commandSocket}/>
        </TabContent>
      </Tabs>
    );
  }
}

export default App;
