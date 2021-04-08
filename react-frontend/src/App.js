import React, { Component } from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";

const upcomingSocket = new W3CWebSocket('ws://127.0.0.1:8091/upcoming');
const findingNameActiveSocket = new W3CWebSocket('ws://127.0.0.1:8091/findingNameActive');
class App extends Component {
  constructor() {
    super()
    this.state = {}
    this.state.upcoming = [];
    this.state.findingNameActive = [];
  }
  
  componentDidMount() {
    upcomingSocket.onopen = () => {
      console.log("/upcoming open")
    };
    upcomingSocket.onclose = () => {
      console.log("/upcoming close")
    }
    upcomingSocket.onmessage = (message) => {
      console.log(message.data);
      const receivedMessage = JSON.parse(message.data);
      this.setState({
        upcoming: receivedMessage
      });
    };

    findingNameActiveSocket.onopen = () => {
      console.log("/findingNameActive open")
    };
    findingNameActiveSocket.onclose = () => {
      console.log("/upfindingNameActivecoming close")
    }
    findingNameActiveSocket.onmessage = (message) => {
      console.log(message.data);
      const receivedMessage = JSON.parse(message.data);
      this.setState({
        findingNameActive: receivedMessage
      });
    };
  }
  
  render() {
    return (

    <div>
      <div>
        upcoming
      </div>
      <div>
      {this.state.upcoming.map(title => (
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