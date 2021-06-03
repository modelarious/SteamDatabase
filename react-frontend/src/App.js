import React, { Component } from 'react';
import Board from 'react-trello'
import SocketContainer from "./SocketContainer.js";
import { FINDING_NAME_ACTIVE_STATE, STATES, UPCOMING_STATE, translate_state_to_title } from './States.js';

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
    const endpoints = STATES.concat([
      "/command",
    ]);

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
    const d = {
    	'lanes': lanes
    }
    
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
