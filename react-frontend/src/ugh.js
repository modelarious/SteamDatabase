import React, { Component } from 'react';
import Board from 'react-trello'
import SocketContainer from "./SocketContainer.js";
const autoBind = require('auto-bind');

const { STATES, FINDING_NAME_ACTIVE_STATE, translate_state_to_title } = require("./States.js");

class App extends Component {
	constructor() {
		super()
		const endpoints = STATES.concat([
			"/command",
		]);

		// XXX Also you should pass in backendServerIP, backendServerPort
		const socketContainer = new SocketContainer(endpoints);
		console.log(socketContainer.sockets);
		console.log("clearing socket states")
		this.socketStates = Object.fromEntries( 
		  STATES.map( name => [name, []]) 
		);
		console.log("Cleared socket states")
		console.log(this.socketStates)

		this.state = {
			data: {
				lanes: [
					{
						id: 'upcoming',
						title: 'Upcoming',
						label: '2/2',
						cards: [
							{id: 'Card1', title: 'Write Blog', description: 'Can AI make memes', label: '30 mins', draggable: false},
							{id: 'Card2', title: 'Pay Rent', description: 'Transfer via NEFT', label: '5 mins', metadata: {sha: 'be312a1'}}
						]
					},
					{
						id: 'COMPLETED',
						title: 'Completed',
						label: '0/0',
						cards: []
					}
				]
			}
		}
		autoBind(this);

		// socketContainer.sockets[FINDING_NAME_ACTIVE_STATE].onmessage = (message) => {
		// 	const receivedArray = JSON.parse(message.data);
		// 	console.log("RECEIVED VALUE")
		// 	console.log(receivedArray)
		// 	this.setSocketState(FINDING_NAME_ACTIVE_STATE, receivedArray);
        //     this.setState(this.builderFunction())
		// 	// console.log(this.socketStates)
		// 	// console.log(this)
		// };
		socketContainer.sockets[FINDING_NAME_ACTIVE_STATE].onmessage = function(message) {
			const receivedArray = JSON.parse(message.data);
			console.log("RECEIVED VALUE")
			console.log(receivedArray)
			this.setSocketState(FINDING_NAME_ACTIVE_STATE, receivedArray);
            this.setState(this.builderFunction())
			// console.log(this.socketStates)
			// console.log(this)
		};
	}

	setSocketState(state, array) {
		this.socketStates[state] = array;
	}

	builderFunction() {
		// update the table once you have updated this.socketStates
		var lanes = [];
		for (const [stateName, currentSocketArray] of Object.entries(this.socketStates)) {
			var cards = [];
			for (const trackedObject of currentSocketArray) {
				cards.push({
					id: trackedObject.gameName, 
					title: trackedObject.gameName, 
					description: trackedObject.gameName, 
					label: trackedObject.gameName, 
					draggable: false
				})
			}
			const stateTitle = translate_state_to_title(stateName) 
			lanes.push({
				id: stateName,
				title: stateTitle,
				// label: `${cards.length}`,
				cards: cards
			})
		}
		return {
			data: {
				'lanes': lanes
			}
		}
	}

	changeState() {
		this.setState(this.builderFunction())
	}
	
	render() {
		return <div>
			<button onClick={this.changeState}>
				Activate Lasers
			</button>
			<Board data={this.state.data}/>
		</div>
	}
}

export default App;
