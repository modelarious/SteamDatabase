import React, { Component } from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";
import SocketContainer from "./SocketContainer.js";
import { FINDING_NAME_ACTIVE_STATE, STATES, UPCOMING_STATE } from './States.js';

const autoBind = require('auto-bind');


// const upcomingSocket = new W3CWebSocket('ws://127.0.0.1:3091/upcoming');
// const findingNameActiveSocket = new W3CWebSocket('ws://127.0.0.1:3091/findingNameActive');
class App extends Component {
  constructor() {
    super()
    this.state = {}
    this.state[UPCOMING_STATE] = [];
    this.state.findingNameActive = [];
		autoBind(this);
  }
  
  componentDidMount() {
		const endpoints = STATES.concat([
			"/command",
		]);

		const socketContainer = new SocketContainer(endpoints);
		
		socketContainer.sockets[UPCOMING_STATE].onmessage = (message) => {
      console.log(message.data);
      const receivedMessage = JSON.parse(message.data);
      this.setState({
        [UPCOMING_STATE]: receivedMessage
      });
    };

    socketContainer.sockets[UPCOMING_STATE].onopen = () => {
      console.log("/UPCOMING_STATE open")
    };
    socketContainer.sockets[UPCOMING_STATE].onclose = () => {
      console.log("/UPCOMING_STATE close")
    }
		socketContainer.sockets[FINDING_NAME_ACTIVE_STATE].onmessage = (message) => {
      console.log(message.data);
      const receivedMessage = JSON.parse(message.data);
      this.setState({
        findingNameActive: receivedMessage
      });
    };

    socketContainer.sockets[FINDING_NAME_ACTIVE_STATE].onopen = () => {
      console.log("/findingNameActive open")
    };
    socketContainer.sockets[FINDING_NAME_ACTIVE_STATE].onclose = () => {
      console.log("/upfindingNameActivecoming close")
    }
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
        Upcoming
      </div>
      <div>
      {this.state[UPCOMING_STATE].map(title => (
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