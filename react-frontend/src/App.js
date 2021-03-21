import React, { Component } from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";

const client = new W3CWebSocket('ws://127.0.0.1:8091/game');

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
      console.log(message);
      const newGame = JSON.parse(message.data).game

      // this.setState(previousState => ({
      //   games: [...previousState.games, ...newGames]
      // }));
      this.setState({
        games: this.state.games.concat(newGame)
      })
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
