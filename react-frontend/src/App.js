import React, { Component } from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";

const client = new W3CWebSocket('ws://127.0.0.1:8091/upcoming');
class App extends Component {
  constructor() {
    super()
    this.state = {}
    this.state.upcoming = [];
  }
  
  componentDidMount() {
    client.onopen = () => {
      console.log("/upcoming open")
    };
    client.onclose = () => {
      console.log("/upcoming close")
    }
    client.onmessage = (message) => {
      console.log(message.data);
      const receivedMessage = JSON.parse(message.data);
      this.setState({
        upcoming: receivedMessage
      });
    };
  }
  
  render() {
    return (

      <div>
      <div>
        upcoming test
      </div>
      <div>
      {this.state.upcoming.map(title => (
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