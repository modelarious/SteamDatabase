import React, { Component } from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";

const client = new W3CWebSocket('ws://127.0.0.1:8091/game');

class App extends Component {
  constructor() {
    super()
    this.state = {}
    this.state.people = [
      { id: 1, name: 'chris' },
      { id: 2, name: 'nick' }
    ];
  }
  
  componentWillMount() {
    client.onopen = () => {
      console.log("open")
      //do stuff
    };
    client.onclose = () => {
      //do stuff
    }
    client.onmessage = (message) => {
      console.log(message);
      const newPerson = JSON.parse(message.data).person
      // this.setState()

      // this.setState(previousState => ({
      //   people: [...previousState.people, ...newPeople]
      // }));
      this.setState({
        people: this.state.people.concat(newPerson)
      })
    };
  }
  
  render() {
    return (

      <div>
      <div>
        Practical Intro To WebSockets.
      </div>
      <div>
      {this.state.people.map(person => (
        <p key={person.id}>{person.name}</p>
      ))}
    </div>
    </div>
    );
  }
}

export default App;
