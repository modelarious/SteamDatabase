import React, { Component } from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";

const client = new W3CWebSocket('ws://127.0.0.1:8091/game');
// const client = new W3CWebSocket('ws://127.0.0.1:8091/upcoming');
class App extends Component {
  constructor() {
    super()
    this.state = {}
    this.state.games = [
      { steamID: "1", steamName: 'factorio' },
      { steamID: "2", steamName: 'satisfactory' }
    ];
  }
  
  componentDidMount() {
    client.onopen = () => {
      console.log("/game open")
    };
    client.onclose = () => {
      console.log("/game close")
    }
    client.onmessage = (message) => {
      const receivedMessage = JSON.parse(message.data);
      console.log(receivedMessage);
      const newGames = receivedMessage.games;
      if (!newGames) {
        throw Error('games field was not defined in ' + message.data);
      }

      this.setState(previousState => ({
        games: [...previousState.games, ...newGames]
      }));
    };
  }
  
  render() {
    return (

      <div>
      <div>
        /game socket test
      </div>
      <div>
      {this.state.games.map(game => (
        <p key={game.steamID}>{game.steamName}</p>
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