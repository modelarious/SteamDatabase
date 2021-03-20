import React, { Component } from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";

const client = new W3CWebSocket('ws://127.0.0.1:8091/game');

class App extends Component {
  constructor() {
    super()
    this.people = [
      { id: 1, name: 'chris' },
      { id: 2, name: 'nick' }
    ];
  }
  
  componentWillMount() {
    client.onopen = () => {
      console.log('WebSocket Client Connected');
    };
    client.onmessage = (message) => {
      console.log(message);
    };
  }
  
  render() {
    return (

      <div>
      <div>
        Practical Intro To WebSockets.
      </div>
      <div>
      {this.people.map(person => (
        <p key={person.id}>{person.name}</p>
      ))}
    </div>
    </div>
    );
  }
}

export default App;
