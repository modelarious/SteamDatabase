import React, { Component } from 'react';
import Dropdown from 'react-dropdown';

import { WithContext as ReactTags } from 'react-tag-input';
const autoBind = require('auto-bind');


function retrieve_name(game) {
    return game.game_name_from_steam;
}
function retrieve_review_score(game) {
    return game.avg_review_score;
}

function string_includes(str, subStr) {
    return str.toLowerCase().includes(subStr.toLowerCase());
}

function greater_than(num, filter_num) {
    return parseInt(num) > parseInt(filter_num);
}
function greater_than_or_equal_to(num, filter_num) {
    return parseInt(num) >= parseInt(filter_num);
}
function less_than(num, filter_num) {
    return parseInt(num) < parseInt(filter_num);
}
function less_than_or_equal_to(num, filter_num) {
    return parseInt(num) <= parseInt(filter_num);
}
function equal(num, filter_num) {
    return parseInt(num) === parseInt(filter_num);
}

class filter {
    constructor(initial_value, filter_boolean_function, game_accessor_function) {
        this.filter_state = initial_value
        this.filter_boolean_function = filter_boolean_function
        this.game_accessor_function = game_accessor_function;
        autoBind(this);
    }

    update_filter_state(new_value) {
        this.filter_state = new_value;
    }

    update_filter_boolean_function(new_function) {
        this.filter_boolean_function = new_function
    }

    _apply_to_game(game) {
        const field_value = this.game_accessor_function(game)
        return this.filter_boolean_function(field_value, this.filter_state)
    }

    apply(games) {
        return games.filter(game => this._apply_to_game(game));
    }
}
// const game_name_filter = new filter("stuff", string_includes, retrieve_name);
// const review_score_filter = new filter(7, greater_than, retrieve_review_score);
// game_name_filter._apply_to_game({ "name": "STUFF IN HERE" });
// game_name_filter.update_filter_boolean_function(always_false);
// game_name_filter._apply_to_game({ "name": "STUFF IN HERE" });


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

const COUNTRIES = ["Thailand", "India", "Vietnam", "Turkey", "USA", "Canada"]
const suggestions = COUNTRIES.map(country => {
  return {
    id: country,
    text: country
  };
});

const KeyCodes = {
  comma: 188,
  enter: 13
};

const delimiters = [KeyCodes.comma, KeyCodes.enter];

const Whoa = () => {
  const [tags, setTags] = React.useState([
    { id: 'Thailand', text: 'Thailand' },
    { id: 'India', text: 'India' },
    { id: 'Vietnam', text: 'Vietnam' },
    { id: 'Turkey', text: 'Turkey' }
  ]);

  const handleDelete = i => {
    setTags(tags.filter((tag, index) => index !== i));
  };

  const handleAddition = tag => {
    setTags([...tags, tag]);
  };

  const onClearAll = () => {
    setTags([]);
  };

  const handleDrag = (tag, currPos, newPos) => {
    const newTags = tags.slice();

    newTags.splice(currPos, 1);
    newTags.splice(newPos, 0, tag);

    // re-render
    setTags(newTags);
  };

  const handleTagClick = index => {
    console.log('The tag at index ' + index + ' was clicked');
  };

  return (
    <div className="app">
      <div>
        <ReactTags
          tags={tags}
          suggestions={suggestions}
          delimiters={delimiters}
          onClearAll={onClearAll}
          handleDelete={handleDelete}
          handleAddition={handleAddition}
          handleDrag={handleDrag}
          handleTagClick={handleTagClick}
          inputFieldPosition="inline"
          placeholder="Genre tags..."
          minQueryLength={1}
          allowDragDrop={false}
          clearAll={true}
          autocomplete
        />
      </div>
    </div>
  );
};


const ratingFilterTypeIndex = {
    "<": greater_than,
    "<=": greater_than_or_equal_to,
    "==": equal,
    ">": less_than,
    ">=": less_than_or_equal_to
}
const ratingFilterTypeOptions = Object.keys(ratingFilterTypeIndex)
const defaultRatingFilterTypeOption = ratingFilterTypeOptions[0];
const GAME_NAME_FILTER = "Game Name Filter";
const REVIEW_SCORE_FILTER = "Review Score Filter";
export default class Filters extends Component {
    constructor(props) {
        super()
        this.onUpdate = props.onUpdate;
        this.getGames = props.getGames;
        this.state = { 
            [GAME_NAME_FILTER]: '',
            [REVIEW_SCORE_FILTER]: -1,
        };
        this.filters = {
            [GAME_NAME_FILTER]: new filter(this.state[GAME_NAME_FILTER], string_includes, retrieve_name),
            [REVIEW_SCORE_FILTER]: new filter(this.state[REVIEW_SCORE_FILTER], ratingFilterTypeIndex[defaultRatingFilterTypeOption], retrieve_review_score),
        };
        autoBind(this);
    }

    _triggerFilterUpdate() {
        const all_games = this.getGames();
        let filtered_games = all_games;
        for (const filter of Object.values(this.filters)) {
            filtered_games = filter.apply(filtered_games);
        }
        this.onUpdate(filtered_games);
    }

    _filterUpdate(event) {
        const new_state = event.target.value;
        const filter_name = event.target.name;
        this.setState({ 
            [filter_name]: new_state
        });
        this.filters[filter_name].update_filter_state(new_state)
        console.log(new_state)
        this._triggerFilterUpdate()
    }

    _onSelectRatingFilterType(ratingFilterTypeChangeEvent) {
        const ratingFilterType = ratingFilterTypeChangeEvent.value;
        const newFilterTypeFunction = ratingFilterTypeIndex[ratingFilterType];
        this.filters[REVIEW_SCORE_FILTER].update_filter_boolean_function(newFilterTypeFunction)
        console.log("Updated filter function to")
        console.log(newFilterTypeFunction)
        this._triggerFilterUpdate()
    }

    render() {

        const style = {
            display: 'flex',
            justifyContent: 'start',
            paddingLeft : '20px'
        };

        return <form>
            <label style={style}>
                <text>{GAME_NAME_FILTER}:</text>
                <input type="text" value={this.state[GAME_NAME_FILTER]} onChange={this._filterUpdate} name={GAME_NAME_FILTER} />
            </label>
            <div style={style}>
                <text>Filter by review score</text>
                <Dropdown options={ratingFilterTypeOptions} onChange={this._onSelectRatingFilterType} value={defaultRatingFilterTypeOption} placeholder="Rating Filter Type" />
                <text>to</text>
                <input type="text" value={this.state[REVIEW_SCORE_FILTER]} onChange={this._filterUpdate} name={REVIEW_SCORE_FILTER} />
            </div>
            <Whoa></Whoa>
            {/* <label>
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
                <input type="text" value={this.state.gameNameFilter} onChange={this._gameNameFilterTextUpdate} name="Controller Support Filter" />
            </label> */}
        </form>
    }
}