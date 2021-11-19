import React, { Component } from 'react';
import SocketContainer from "./SocketContainer.js";
import { STATES, AWAITING_USER_STATE } from './States.js';
import {
  TabLink,
  Tabs,
  TabContent
} from 'react-tabs-redux';
import GameFactory from "./Factories/GameFactory";
import DebugBoard from './Views/DebugBoard';
import GameListView from './Views/GameListView';
const autoBind = require('auto-bind');

const COMMAND = "/command";
const GAMES = "/games";
const endpoints = STATES.concat([
  COMMAND,
  GAMES
]);

// XXX I really don't like this being global - but it seems to be the only way to
// establish these connections before the first render call triggers
const socketContainer = new SocketContainer(endpoints);

class App extends Component {
  constructor() {
    super();
    this.state = {};
    for (const state of STATES.concat([GAMES])) {
      this.state[state] = [];
    }
    this.socketContainer = socketContainer;
    autoBind(this);
  }
  
  componentDidMount() {
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
    var debugBoardNeededStateData = {}
    for (const stateName of STATES) {
      debugBoardNeededStateData[stateName] = this.state[stateName];
    }

    let commandSocket;
    if (this.socketContainer) {
      commandSocket = this.socketContainer.get_socket(COMMAND)
    }

    let userInputSocket;
    if (this.socketContainer) {
      userInputSocket = this.socketContainer.get_socket(AWAITING_USER_STATE)
    }

    let userInputRequiredArray;
    if (this.socketContainer) {
      userInputRequiredArray = this.state[AWAITING_USER_STATE];
    }

    const game_factory = new GameFactory()
    const games = this.state[GAMES].map(
      game_from_backend => game_factory.create_game(game_from_backend)
    );
    console.log(games)

    return (
      <Tabs renderActiveTabContentOnly={true}>
        <TabLink to="tab1" default>Games</TabLink>
        <TabLink to="tab2">User Input</TabLink>
        <TabLink to="tab3">Debug</TabLink>
      
        <TabContent for="tab1">
          <GameListView key={games} games={games} updateScrollDistance={this.scrollDistanceUpdate}></GameListView>
        </TabContent>
        <TabContent for="tab2">
          <UserInputView userInputRequiredArray={userInputRequiredArray} userInputSocket={userInputSocket}></UserInputView>
        </TabContent>
        <TabContent for="tab3">
          <DebugBoard stateData={debugBoardNeededStateData} commandSocket={commandSocket}/>
        </TabContent>
      </Tabs>
    );
  }
}


class UserInputView extends Component {
  constructor(props) {
    super();
    this.state = {
      games : props.userInputRequiredArray,
      possible_selections : []
    };
    this.user_input_socket = props.userInputSocket;
    this.current_game_title = undefined;
    autoBind(this);
  }

  select_game(event) {
    const game_title = event.target.outerText;
    let currgame = undefined;
    for (const game of this.state.games) {
      if (game.game_name_on_disk === game_title) {
        currgame = game;
        break;
      }
    }
    if (!currgame) {
      console.error(`couldn't find game ${game_title} in ${JSON.stringify(this.state.games)}`)
      return;
    }
    const possible_selections = currgame.possible_matches_list.map(
      possible_match => possible_match.steam_name
    )
    this.current_game_title = game_title;
    this.setState({
      possible_selections : possible_selections
    })
    // list of full objects instead of just game titles
    this.possible_selections_full = currgame.possible_matches_list;
  }

  _search(steam_game_title) {
    for (const suggested_match of this.possible_selections_full) {
      if (suggested_match.steam_name === steam_game_title) {
        return suggested_match.steam_id_number;
      }
    }
  }
  
  select_matching_steam_game(event) {
    const steam_game_title = event.target.outerText;
    const steam_id = this._search(steam_game_title);
    if (steam_id) {
      this.user_input_socket.send(JSON.stringify({
        game_name_on_disk : this.current_game_title,
        game_name_from_steam : steam_game_title,
        steam_id_number : steam_id
      }))

      this.setState({
        possible_selections : []
      })
      this.possible_selections_full = [];
      this.current_game_title = undefined;
    } else {
      console.log(`FAILURE!!!!!!! game_name == ${steam_game_title}, current_game_title= ${this.current_game_title}, steam_id = ${steam_id}`)
    }
  }

  // XXX is the second list ordered by match score?
  render() {
    const available_titles = this.state.games.map(
      game => game.game_name_on_disk
    )
    return <span>
      <h1>Current Game:</h1>
      <ListComponent onClick={this.select_game} items={available_titles}/>
      <hr></hr>
      <h1>Possible matches:</h1>
      <ListComponent onClick={this.select_matching_steam_game} items={this.state.possible_selections}/>
    </span>
  }
}

// function UserInputView(props) {
//   const games = props.userInputRequiredArray;
//   const userInputSocket = props.userInputSocket;

//   function select_game(event) {
//     console.log(event.target.outerText)
//   }
  
//   function select_matching_steam_game(event) {
//     console.log(event.target.outerText)
//     console.log("Match")
//   }

//   console.log(props.userInputRequiredArray)
//   for (const game of games) {
//     console.log(game.game_name_on_disk);
//     console.log(game.possible_matches_list)
//   }
  
//   return <span>
//     <h1>Current Game:</h1>
//     <ListComponent onClick={select_game} items={["hello","jh","wege"]}/>
//     <hr></hr>
//     <h1>Possible choices:</h1>
//     <ListComponent onClick={select_matching_steam_game} items={["hello","jh","wege"]}/>
//   </span>
// }

function ListComponent(props) {
  let array = [];
  for(let i = 0; i < props.items.length; i++) {
    array.push(
      <li key={i} item={props.items[i]} onClick={props.onClick}> {props.items[i]} </li>
    );
  }

  return (
    <ul>
      {array}
    </ul>
  );
}

export default App;
