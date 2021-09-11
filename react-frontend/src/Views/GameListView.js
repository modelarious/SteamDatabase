import React, { Component } from 'react';
import { BrowserRouter, Switch, Route } from "react-router-dom";
import GameView from "./GameView";
import { Home } from './Home';
import Filters from "./Filters";
// import { PageTransition } from "@steveeeie/react-page-transition";

import 'react-dropdown/style.css';
import { Sorter } from '../Sorting/Sorter';
const autoBind = require('auto-bind');


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
                    <Filters></Filters>
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
