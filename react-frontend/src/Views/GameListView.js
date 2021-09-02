import React, { Component } from 'react';
import { BrowserRouter, Switch, Route, Link } from "react-router-dom";
import GameView from "./GameView";
// import { PageTransition } from "@steveeeie/react-page-transition";

const autoBind = require('auto-bind');


function Links(props) {
  return props.games.map((game) => (
    <Link to={`/games/${game.steam_id}`}>
      <img
        alt={`${game.game_name_on_steam} link`}
        src={game.app_detail.header_image_url}
      />
    </Link>
  ));
}

class Home extends Component {
  constructor(props) {
    super();
    this.games = props.games;
    this.updateScrollDistanceMethod = props.updateScrollDistanceMethod;
    this.currentScrollTop = props.currentScrollTop
    autoBind(this);
  }

  // https://stackoverflow.com/questions/53158796/get-scroll-position-with-reactjs
  componentDidMount() {
    window.scrollTo(0, this.currentScrollTop)
    window.addEventListener('scroll', this.listenToScroll)
  }
  
  componentWillUnmount() {
    window.removeEventListener('scroll', this.listenToScroll)
  }
  
  listenToScroll = () => {
    const winScroll =
      document.body.scrollTop || document.documentElement.scrollTop

    this.updateScrollDistanceMethod(winScroll)
  }

  render() {
    return <Links games={this.games} />;
  }
}

class GameListView extends Component {
  constructor(props) {
    super();
    this.games = props.games;
    autoBind(this);
  }

  scrollDistanceUpdate(currentPixelsFromTop) {
    console.log("ooooooh yeah jerry, I got CALLED!");
    console.log(currentPixelsFromTop);
    this.pixelsFromTop = currentPixelsFromTop;
  }

  render() {
    return (
      <React.StrictMode>
        <BrowserRouter>
          {/* Tabs go here and wrap the Route component - this is where I took Links from  */}
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
                    <Home games={this.games} updateScrollDistanceMethod={this.scrollDistanceUpdate} currentScrollTop={this.pixelsFromTop}/>
                  </Route>
                  <Route path="/games/:steam_id">
                    <GameView games={this.games} />
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
