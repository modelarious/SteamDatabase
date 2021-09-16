import React, { Component } from 'react';
const autoBind = require('auto-bind');


function retrieve_name(game) {
    return game.name;
}
function retrieve_review_score(game) {
    return game.avg_review_score;
}

function string_includes(str, subStr) {
    return str.toLowerCase().includes(subStr.toLowerCase());
}
function greater_than(num, filter_num) {
    return num > filter_num;
}
function less_than(num, filter_num) {
    return num < filter_num;
}
function equal(num, filter_num) {
    return num === filter_num;
}

function always_false(str, subStr) {
    return false;
}

class filter {
    constructor(initial_value, filter_boolean_function, game_accessor_function) {
        this.filter_state = initial_value
        this.filter_boolean_function = filter_boolean_function
        this.game_accessor_function = game_accessor_function
    }

    update_filter_state(new_value) {
        this.filter_state = new_value;
    }

    update_filter_boolean_function(new_function) {
        this.filter_boolean_function = new_function
    }

    apply(game) {
        const field_value = this.game_accessor_function(game)
        return this.filter_boolean_function(field_value, this.filter_state)
    }
}
const game_name_filter = new filter("stuff", string_includes, retrieve_name);
const review_score_filter = new filter(7, greater_than, retrieve_review_score);
game_name_filter.apply({ "name": "STUFF IN HERE" });
game_name_filter.update_filter_boolean_function(always_false);
game_name_filter.apply({ "name": "STUFF IN HERE" });


// partial string match            game_name
// numeric comparison              review_score
// partial string match in list    genres, developers, publishers
// Boolean                         controller support

/*
Filters:
    Game Name - includes:
        game_name_on_disk
        game_name_from_steam
    Review Score - <=, >=, ==
        avg_review_score
    Genres - includes:
        user_defined_genres
        genres
    Developers - includes:
        developers
    Publishers - includes:
        publishers
    Controller Support
        controller_support
Sorting - Ascending, Descending
    Game Name
    Review Score
*/
export default class Filters extends Component {
    constructor(onUpdate) {
        super()
        this.state = { 
            gameNameFilter: '',
        };
        this.onUpdate = onUpdate;
        this.filters = [];
        autoBind(this);
    }

    _gameNameFilterTextUpdate(event) {
        const new_state = event.target.value
        this.setState({ 
            gameNameFilter: new_state
        });
        game_name_filter.update_filter_state(new_state)
        console.log(new_state)
        // this.onUpdate()
    }

    render() {
        return <form>
            <label>
                Game Name Filter:
                <input key={this.state.gameNameFilter} type="text" value={this.state.gameNameFilter} onChange={this._gameNameFilterTextUpdate} name="Game Name Filter" />
            </label>
            {/* <label>
                Review Score Filter:
                <input type="text" value={this.state.gameNameFilter} onChange={this._gameNameFilterTextUpdate} name="Review Score Filter" />
            </label>
            <label>
                Genre Filter:
                <input type="text" value={this.state.gameNameFilter} onChange={this._gameNameFilterTextUpdate} name="Genre Filter" />
            </label> */}
            {/* <label>
                Developer Filter:
                <input type="text" value={this.state.gameNameFilter} onChange={this._gameNameFilterTextUpdate} name="Developer Filter" />
            </label>
            <label>
                Publisher Filter:
                <input type="text" value={this.state.gameNameFilter} onChange={this._gameNameFilterTextUpdate} name="Publisher Filter" />
            </label> */}
            {/* <label>
                Controller Support Filter:
                <input type="text" value={this.state.gameNameFilter} onChange={this._gameNameFilterTextUpdate} name="Publisher Filter" />
            </label> */}
        </form>
    }
}