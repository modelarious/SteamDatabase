import React, { Component } from 'react';
import { BrowserRouter, Switch, Route } from "react-router-dom";
import GameView from "./GameView";
import { Home } from './Home';
// import { PageTransition } from "@steveeeie/react-page-transition";

import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';
import { ascendingSortingStrategy } from '../Sorting/Strategies/ascendingSortingStrategy';

const autoBind = require('auto-bind');

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


class Sorter extends Component {
  constructor(onUpdate) {
    super();
    this.sortingField = sortingFieldsIndex[defaultSortFieldOption];
    this.sortingStrategy = sortingStrategiesIndex[defaultSortStrategyOption];
    this.onUpdate = onUpdate;
    autoBind(this);
  }

  _onSelectSortStrategy(sortStrategy) {
    const sortingStrategy = sortStrategy.value;
    this.sortingStrategy = sortingStrategiesIndex[sortingStrategy];
    this.onUpdate();
  }

  _onSelectSortField(sortField) {
    const sortingField = sortField.value;
    this.sortingField = sortingFieldsIndex[sortingField];
    this.onUpdate();
  }
  
  getSortedValues(games) {
    console.log(`sorting by ${this.sortingField}, using ${this.sortingStrategy.get_name()} strategy`);
    return this.sortingStrategy.sortGames(games, this.sortingField)
  }

  render() {
    return <div>
      <Dropdown options={sortingStrategyOptions} onChange={this._onSelectSortStrategy} value={defaultSortStrategyOption} placeholder="Sort Strategy" />
      <Dropdown options={sortingFieldOptions} onChange={this._onSelectSortField} value={defaultSortFieldOption} placeholder="Sort Type" />
    </div>
  }
}

// XXX will this reconstruct when app.state.games has a game added to it?
class GameListView extends Component {
  constructor(props) {
    super();
    autoBind(this);
    this.sorter = new Sorter(this._onUpdate);
    this.state = {
      games: props.games
    };
  }

  scrollDistanceUpdate(currentPixelsFromTop) {
    this.pixelsFromTop = currentPixelsFromTop;
  }

  _getFilteredValues(games) {
    return games;
  }

  _onUpdate() {
    const filtered = this._getFilteredValues(this.state.games);
    const sorted = this.sorter.getSortedValues(filtered);
    console.log("Sorted games:")
    console.log(sorted)
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
                    {this.sorter.render()}
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
