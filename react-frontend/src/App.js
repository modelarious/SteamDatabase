import React, { Component } from 'react';
import Board from 'react-trello'
import SocketContainer from "./SocketContainer.js";
import { FINDING_NAME_ACTIVE_STATE, STATES, UPCOMING_STATE, translate_state_to_title } from './States.js';

const autoBind = require('auto-bind');


// const upcomingSocket = new W3CWebSocket('ws://127.0.0.1:3091/upcoming');
// const findingNameActiveSocket = new W3CWebSocket('ws://127.0.0.1:3091/findingNameActive');
class App extends Component {
  constructor() {
    super()
    this.state = {}
    this.state.tracking = {}
    this.state[UPCOMING_STATE] = [];
    this.state[FINDING_NAME_ACTIVE_STATE] = [];
    autoBind(this);
  }
  
  componentDidMount() {
    const endpoints = STATES.concat([
      "/command",
    ]);

    const socketContainer = new SocketContainer(endpoints);
    
    socketContainer.sockets[UPCOMING_STATE].onmessage = (message) => {
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
      const receivedMessage = JSON.parse(message.data);
      this.setState({
        [FINDING_NAME_ACTIVE_STATE]: receivedMessage
      });
    };

    socketContainer.sockets[FINDING_NAME_ACTIVE_STATE].onopen = () => {
      console.log("/FINDING_NAME_ACTIVE_STATE open")
    };
    socketContainer.sockets[FINDING_NAME_ACTIVE_STATE].onclose = () => {
      console.log("/FINDING_NAME_ACTIVE_STATE close")
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
    var lanes = [];
    for (const [stateName, currentSocketArray] of Object.entries({
    	[UPCOMING_STATE]: this.state[UPCOMING_STATE],
    	[FINDING_NAME_ACTIVE_STATE]: this.state[FINDING_NAME_ACTIVE_STATE],
    })) {
    	var cards = [];
    	for (const trackedObject of currentSocketArray) {
    		cards.push({
    			// id: trackedObject.gameName, 
    			// title: trackedObject.gameName, 
    			// description: trackedObject.gameName, 
    			// label: trackedObject.gameName, 
    			id: trackedObject, 
    			title: trackedObject, 
    			description: trackedObject, 
    			label: trackedObject, 
    			draggable: false
    		})
    	}
    	const stateTitle = translate_state_to_title(stateName) 
    	lanes.push({
    		id: stateName,
    		title: stateTitle,
    		label: stateTitle,
    		// label: `${cards.length}`,
    		cards: cards
    	})
    }

    console.log(lanes)
    const d = {
    	'lanes': lanes
    }

    console.log(d);
    
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
        {this.state[FINDING_NAME_ACTIVE_STATE].map(title => (
          <p key={title}>{title}</p>
        ))}
      </div>
      <Board data={d}/>
    </div>
    );
  }
}

export default App;
