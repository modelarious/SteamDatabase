import React, { Component } from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";
import SocketContainer from "./SocketContainer.js";
import { FINDING_NAME_ACTIVE_STATE } from './States.js';

const autoBind = require('auto-bind');


const upcomingSocket = new W3CWebSocket('ws://127.0.0.1:3091/upcoming');
// const findingNameActiveSocket = new W3CWebSocket('ws://127.0.0.1:3091/findingNameActive');
class App extends Component {
  constructor() {
    super()
    this.state = {}
    this.state.awaitingUser = [];
    this.state.findingNameActive = [];
		autoBind(this);
  }
  
  componentDidMount() {
    upcomingSocket.onopen = () => {
      console.log("/awaitingUser open")
    };
    upcomingSocket.onclose = () => {
      console.log("/awaitingUser close")
    }
    upcomingSocket.onmessage = (message) => {
      console.log(message.data);
      const receivedMessage = JSON.parse(message.data);
      this.setState({
        awaitingUser: receivedMessage
      });
    };

    // findingNameActiveSocket.onopen = () => {
    //   console.log("/findingNameActive open")
    // };
    // findingNameActiveSocket.onclose = () => {
    //   console.log("/upfindingNameActivecoming close")
    // }
    // findingNameActiveSocket.onmessage = (message) => {
    //   console.log(message.data);
    //   const receivedMessage = JSON.parse(message.data);
    //   this.setState({
    //     findingNameActive: receivedMessage
    //   });
    // };

		const endpoints = [
			"/findingNameActive",
			"/infoRetrievalActive",
			"/stored",
			"/command",
			"/awaitingUser",
			"/queuedForInfoRetrieval"
		];
		const socketContainer = new SocketContainer(endpoints);
		socketContainer.sockets[FINDING_NAME_ACTIVE_STATE].onmessage = (message) => {
      console.log(message.data);
      const receivedMessage = JSON.parse(message.data);
      this.setState({
        findingNameActive: receivedMessage
      });
    };
		// console.log(socketContainer.sockets);
		// console.log("clearing socket states");
		// this.socketStates = Object.fromEntries( 
		//   endpoints.map( name => [name, []]) 
		// );
		// console.log("Cleared socket states")
		// console.log(this.socketStates)
  }
  
  render() {
    return (

    <div>
      <div>
        awaitingUser
      </div>
      <div>
      {this.state.awaitingUser.map(title => (
        <p key={title}>{title}</p>
      ))}
      </div>
      <hr></hr>
      <div>
        FindingNameActive
      </div>
      <div>
        {this.state.findingNameActive.map(title => (
          <p key={title}>{title}</p>
        ))}
      </div>
    </div>
    );
  }
}

export default App;
//states:
// - todo
// - finding name (active)
// - awaiting user input
// - queued for info retrieval
// - info retrieval (active)
// - stored