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
      <div style={{ 
        backgroundImage: `url("https://cdn.akamai.steamstatic.com/steam/apps/313010/page_bg_generated_v6b.jpg?t=1602859660")`,
        backgroundRepeat: 'no-repeat',
        backgroundColor: '#1c2838'
      }}>
        <Tabs renderActiveTabContentOnly={true}>
          <TabLink to="tab1" default>Games</TabLink>
          <TabLink to="tab2">User Input</TabLink>
          <TabLink to="tab3">Debug</TabLink>
        
          <TabContent for="tab1">
            <GameListView games={this.state[GAMES]}></GameListView>
          </TabContent>
          <TabContent for="tab2">"user input view"</TabContent>
          <TabContent for="tab3">
            <DebugBoard stateData={debugBoardNeededStateData} commandSocket={commandSocket}/>
          </TabContent>
        </Tabs>
      </div>
    );
  }
}

export default App;
