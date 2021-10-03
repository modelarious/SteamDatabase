import React, { Component } from 'react';
import { BrowserRouter, Switch, Route } from "react-router-dom";
import GameView from "./GameView";
import { Home } from './Home';
import Filters from "./Filters";
// import { PageTransition } from "@steveeeie/react-page-transition";

import 'react-dropdown/style.css';
import { Sorter } from '../Sorting/Sorter';
const autoBind = require('auto-bind');

class GameListView extends Component {
  constructor(props) {
    super();
    autoBind(this);

    // Sorter MUST be defined after autoBind is called since we are passing in a function and javascript is stupid about
    // how it handles this.* accesses inside of passed in functions
    this.sorter = new Sorter(this._onSortUpdate);
    this.state = {
      games: props.games,
      display_games: props.games
    };
  }

  _scrollDistanceUpdate(currentPixelsFromTop) {
    this.pixelsFromTop = currentPixelsFromTop;
  }

  _onSortUpdate() {
    const sorted = this.sorter.getSortedValues(this.state.display_games);
    this.setState({
      display_games: sorted
    })
  }

  _onUpdate(filtered_games) {
    const sorted = this.sorter.getSortedValues(filtered_games)
    this.setState({
      display_games: sorted
    })
  }

  _getGames() {
    return this.state.games;
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
                    <Filters onUpdate={this._onUpdate} getGames={this._getGames}></Filters>
                    <Home key={this.state.display_games} games={this.state.display_games} updateScrollDistanceMethod={this._scrollDistanceUpdate} currentScrollTop={this.pixelsFromTop}/>
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
