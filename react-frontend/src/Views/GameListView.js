import React, { Component } from 'react';
import { BrowserRouter, Switch, Route } from "react-router-dom";
import GameView from "./GameView";
import { Home } from './Home';
// import { PageTransition } from "@steveeeie/react-page-transition";

import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';

const autoBind = require('auto-bind');

// https://stackoverflow.com/a/2466503
var byField = function (field) {
  return function (a, b) {
    if (typeof a[field] == "number") {
      return (b[field] - a[field]);
    } else {
      return ((a[field] < b[field]) ? -1 : ((a[field] > b[field]) ? 1 : 0));
    }
  };
};

class ascendingSortingStrategy {
  constructor() {
    this._name = "Ascending";
    autoBind(this);
  }
  get_name() {
    return this._name;
  }
  sortGames(games, field) {
    const games_copy = JSON.parse(JSON.stringify(games));
    games_copy.sort(byField(field))
    return games_copy;
  }
}

const ascendingStrategy = new ascendingSortingStrategy();
const sortingStrategies = [
  ascendingStrategy
];


let sortingStrategiesIndex = {}
for (const strategy of sortingStrategies) {
  sortingStrategiesIndex[strategy.get_name()] = strategy;
}
const sortingStrategyOptions = sortingStrategies.map(
  strat => strat.get_name()
)
const defaultSortStrategyOption = ascendingStrategy.get_name();





const sortingFieldsIndex = {
  "Steam Game Title": "game_name_from_steam",
  "Steam Average Review Score": "avg_review_score",
}

const sortingFieldOptions = Object.keys(sortingFieldsIndex)
const defaultSortFieldOption = sortingFieldOptions[0];




// will this reconstruct when app.state.games has a game added to it?
class GameListView extends Component {
  constructor(props) {
    super();
    this.sortingField = sortingFieldsIndex[defaultSortFieldOption];
    this.sortingStrategy = sortingStrategiesIndex[defaultSortStrategyOption];
    autoBind(this);
    this.state = {
      games: this._getSortedValues(props.games)
    };
  }

  scrollDistanceUpdate(currentPixelsFromTop) {
    this.pixelsFromTop = currentPixelsFromTop;
  }

  _onSelectSortStrategy(sortStrategy) {
    const sortingStrategy = sortStrategy.value;
    this.sortingStrategy = sortingStrategiesIndex[sortingStrategy];
    this._onSortUpdate();
  }

  _onSelectSortField(sortField) {
    const sortingField = sortField.value;
    this.sortingField = sortingFieldsIndex[sortingField];
    this._onSortUpdate();
  }
  
  _getSortedValues(games) {
    console.log(`sorting by ${this.sortingField}, using ${this.sortingStrategy.get_name()} strategy`);
    return this.sortingStrategy.sortGames(games, this.sortingField)
  }
  
  _onSortUpdate() {
    const sorted = this._getSortedValues(this.state.games);
    this.setState({
      games: sorted,
    })
  }

  render() {
    return (
      <React.StrictMode>
        <BrowserRouter>
          <Route
            render={({ location }) => {
              return (
                // <PageTransition
                // transitionKey={location.pathname}
                // enterAnimation="moveFromTopFade"
                // exitAnimation="moveToBottomFade"
                // >
                <Switch location={location}>
                  <Route exact path="/">
                    <Dropdown options={sortingStrategyOptions} onChange={this._onSelectSortStrategy} value={defaultSortStrategyOption} placeholder="Sort Strategy" />
                    <Dropdown options={sortingFieldOptions} onChange={this._onSelectSortField} value={defaultSortFieldOption} placeholder="Sort Type" />
                    <Home key={this.state.games} games={this.state.games} updateScrollDistanceMethod={this.scrollDistanceUpdate} currentScrollTop={this.pixelsFromTop}/>
                  </Route>
                  <Route path="/games/:steam_id">
                    <GameView games={this.state.games} />
                  </Route>
                </Switch>
                // </PageTransition>
              );
            }}
          />
        </BrowserRouter>
      </React.StrictMode>
    );
  }
}

export default GameListView;
