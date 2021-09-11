import React, { Component } from 'react';
const autoBind = require('auto-bind');
/*
Filters:
    Game Name - Contains:
        game_name_on_disk
        game_name_from_steam
        path_on_harddrive
    Review Score - <=, >=, ==
        avg_review_score
    Genres - Contains:
        user_defined_genres
        genres
    Developers - Contains:
        developers
    Publishers - Contains:
        publishers
    Controller Support
        controller_support
Sorting - Ascending, Descending
    Game Name
    Review Score
*/

export default class Filters extends Component {
    constructor() {
        super()
        this.state = { 
            gameNameFilter: '', 
        };
        autoBind(this);
    }

    _gameNameFilterTextUpdate(event) {
        this.setState({ 
            gameNameFilter: event.target.value
        });
        console.log(event.target.value)
    }

    gameNameFilterUpdate

    render() {
        return <form>
            <label>
                Game Name Filter:
                <input type="text" value={this.state.gameNameFilter} onChange={this._gameNameFilterTextUpdate} name="Game Name Filter" />
            </label>
        </form>
    }
}