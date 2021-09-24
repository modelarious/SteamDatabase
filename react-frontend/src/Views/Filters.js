import React, { Component } from 'react';
import Dropdown from 'react-dropdown';
import { GenreTagSelector } from './GenreTagSelector';
import { greater_than, greater_than_or_equal_to, equal, less_than, less_than_or_equal_to, string_includes, retrieve_name, retrieve_review_score, all_genres_apply_to_game, retrieve_genres, retrieve_controller_support, exists_in_boolean_list } from './filter_functions';
import { filter } from './filter';
const autoBind = require('auto-bind');

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
const GENRE_TAG_FILTER = "Genre Tag Filter";
const CONTROLLER_SUPPORT_FILTER = "Controller Support";
export default class Filters extends Component {
    constructor(props) {
        super()
        this.onUpdate = props.onUpdate;
        this.getGames = props.getGames;
        // XXX there has got to be a better way to set these up than needing 3 references to each constant here, and a bunch of references below
        this.state = { 
            [GAME_NAME_FILTER]: '',
            [REVIEW_SCORE_FILTER]: -1,
            [GENRE_TAG_FILTER]: [],
            [CONTROLLER_SUPPORT_FILTER]: [true, false],
        };
        this.filters = {
            [GAME_NAME_FILTER]: new filter(this.state[GAME_NAME_FILTER], string_includes, retrieve_name),
            [REVIEW_SCORE_FILTER]: new filter(this.state[REVIEW_SCORE_FILTER], ratingFilterTypeIndex[defaultRatingFilterTypeOption], retrieve_review_score),
            [GENRE_TAG_FILTER]: new filter(this.state[GENRE_TAG_FILTER], all_genres_apply_to_game, retrieve_genres),
            [CONTROLLER_SUPPORT_FILTER]: new filter(this.state[CONTROLLER_SUPPORT_FILTER], exists_in_boolean_list, retrieve_controller_support),
        };
        autoBind(this);
    }
    _getFilteredGames() {
        let filtered_games = this.getGames();
        for (const filter of Object.values(this.filters)) {
            filtered_games = filter.apply(filtered_games);
        }
        return filtered_games;
    }

    _triggerFilterUpdate() {
        this.onUpdate(this._getFilteredGames());
    }

    _filterUpdate(event) {
        const new_state = event.target.value;
        const filter_name = event.target.name;
        this.filters[filter_name].update_filter_state(new_state)
        this.setState({ 
            [filter_name]: new_state
        });
        this._triggerFilterUpdate()
    }

    _onSelectRatingFilterType(ratingFilterTypeChangeEvent) {
        const ratingFilterType = ratingFilterTypeChangeEvent.value;
        const newFilterTypeFunction = ratingFilterTypeIndex[ratingFilterType];
        this.filters[REVIEW_SCORE_FILTER].update_filter_boolean_function(newFilterTypeFunction);
        this._triggerFilterUpdate()
    }

    _onUpdateGenreTags(newTags) {
        this.filters[GENRE_TAG_FILTER].update_filter_state(newTags);
        this.setState({ 
            [GENRE_TAG_FILTER]: newTags
        });
        this._triggerFilterUpdate()
    }

    _onRadioUpdate(event) {
        const state = event.target.defaultValue;
        let state_update;

        // only doing this because there are never going to be more than 3 states here - in an ideal world, the event would know what to do with itself
        // instead of me having to figure it out here - I'd just inspect something like event.new_state
        switch(state) {
            case 'Yes':
                state_update = [true];
                break;
            case 'No':
                state_update = [false];
                break;
            case 'Off':
                state_update = [true, false];
                break;
            default:
                console.log("wow... you've really messed up!!")
        }
        this.filters[CONTROLLER_SUPPORT_FILTER].update_filter_state(state_update);
        this.setState({ 
            [CONTROLLER_SUPPORT_FILTER]: state_update
        });
        this._triggerFilterUpdate()
    }

    render() {

        const style = {
            display: 'flex',
            justifyContent: 'start',
            paddingLeft : '20px'
        };

        // XXX could include more genres here from app_detail -- don't forget to change the retrieve_genres function if you update this
        const genre_tags = new Set(this._getFilteredGames().map(game => game.user_defined_genres).flat(Infinity));

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
            <GenreTagSelector genre_tags={genre_tags} onUpdate={this._onUpdateGenreTags}></GenreTagSelector>
            <div>
                <text>Controller support?</text>
                <input type="radio" value="Yes" name="controller_support" onChange={this._onRadioUpdate} /> Yes
                <input type="radio" value="No" name="controller_support" onChange={this._onRadioUpdate} /> No
                <input type="radio" value="Off" name="controller_support" onChange={this._onRadioUpdate} defaultChecked /> Off
            </div>
        </form>
    }
}