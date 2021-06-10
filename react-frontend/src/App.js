import React, { Component } from 'react';
import SocketContainer from "./SocketContainer.js";
import { STATES } from './States.js';
import {
  TabLink,
  Tabs,
  TabContent
} from 'react-tabs-redux';
import DebugBoard from './Views/DebugBoard';

const autoBind = require('auto-bind');

class App extends Component {
  constructor() {
    super();
    this.state = {};
    for (const state of STATES) {
      this.state[state] = [];
    }
    autoBind(this);
  }
  
  componentDidMount() {
    // const endpoints = STATES.concat([
    //   "/command",
    // ]);
    const endpoints = STATES;

    const socketContainer = new SocketContainer(endpoints);
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

    return (
      <Tabs renderActiveTabContentOnly={true}>
        <TabLink to="tab1">Games</TabLink>
        <TabLink to="tab2">User Input</TabLink>
        <TabLink to="tab3" default>Debug</TabLink>
      
        <TabContent for="tab1"> "games view"</TabContent>
        <TabContent for="tab2">"user input view"</TabContent>
        <TabContent for="tab3">
          <DebugBoard stateData={debugBoardNeededStateData}/>
        </TabContent>
      </Tabs>
    );
  }
}

export default App;
