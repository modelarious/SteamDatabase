import React, { Component } from 'react';
const autoBind = require('auto-bind');

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

export class UserInputView extends Component {
  constructor(props) {
    super();
    this.state = {
      games: props.userInputRequiredArray,
      possible_selections: []
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
      console.error(`couldn't find game ${game_title} in ${JSON.stringify(this.state.games)}`);
      return;
    }
    const possible_selections = currgame.possible_matches_list.map(
      possible_match => possible_match.steam_name
    );
    this.current_game_title = game_title;
    this.setState({
      possible_selections: possible_selections
    });
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
        game_name_on_disk: this.current_game_title,
        game_name_from_steam: steam_game_title,
        steam_id_number: steam_id
      }));

      this.setState({
        possible_selections: []
      });
      this.possible_selections_full = [];
      this.current_game_title = undefined;
    } else {
      console.log(`FAILURE!!!!!!! game_name == ${steam_game_title}, current_game_title= ${this.current_game_title}, steam_id = ${steam_id}`);
    }
  }

  // XXX is the second list ordered by match score?
  render() {
    const available_titles = this.state.games.map(
      game => game.game_name_on_disk
    );
    return <span>
      <h1>Current Game:</h1>
      <ListComponent onClick={this.select_game} items={available_titles} />
      <hr></hr>
      <h1>Possible matches:</h1>
      <ListComponent onClick={this.select_matching_steam_game} items={this.state.possible_selections} />
    </span>;
  }
}
