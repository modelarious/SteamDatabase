import React, { Component } from 'react';
import SocketContainer from "./SocketContainer.js";
import { STATES } from './States.js';
import {
  TabLink,
  Tabs,
  TabContent
} from 'react-tabs-redux';
import DebugBoard from './Views/DebugBoard';
import GameListView from './Views/GameListView';
const autoBind = require('auto-bind');
const COMMAND = "/command";
const GAMES = "/games";
const endpoints = STATES.concat([
  COMMAND,
  GAMES
]);

class GameFactory {
  create_game(game_from_backend) {
    const app_detail_subsection = game_from_backend['app_detail'];
    const screenshot_urls = app_detail_subsection['screenshot_urls'].map(
      screenshot_url_incoming => new ScreenshotURL(
        screenshot_url_incoming['thumbnail_url'],
        screenshot_url_incoming['fullsize_url']
      )
    );
    const app_detail = new AppDetail(
      app_detail_subsection['detailed_description'],
      app_detail_subsection['about_the_game'],
      app_detail_subsection['short_description'],
      app_detail_subsection['header_image_url'],
      app_detail_subsection['developers'],
      app_detail_subsection['publishers'],
      app_detail_subsection['metacritic_score'],
      app_detail_subsection['controller_support'],
      app_detail_subsection['genres'],
      screenshot_urls,
      app_detail_subsection['background_image_url']
    );
    return new Game(
      game_from_backend['game_name_on_disk'],
      game_from_backend['game_name_from_steam'],
      game_from_backend['steam_id'],
      game_from_backend['path_on_harddrive'],
      game_from_backend['avg_review_score'],
      game_from_backend['user_defined_genres'],
      app_detail
    );
  }
}

/*
@dataclass
class Game(SteamSendable):
    game_name_on_disk: str
    game_name_from_steam: str
    steam_id: int
    path_on_harddrive: str
    avg_review_score: int
    user_defined_genres: List[str]
    app_detail : AppDetail
*/
class Game {
  constructor(
    game_name_on_disk,
    game_name_from_steam,
    steam_id,
    path_on_harddrive,
    avg_review_score,
    user_defined_genres,
    app_detail) {
      this.game_name_on_disk = game_name_on_disk
      this.game_name_from_steam = game_name_from_steam
      this.steam_id = steam_id
      this.path_on_harddrive = path_on_harddrive
      this.avg_review_score = avg_review_score
      this.user_defined_genres = user_defined_genres
      this.app_detail = app_detail
    }
}

/*
@dataclass
class ScreenshotURL:
	thumbnail_url: str
	fullsize_url: str
*/
class ScreenshotURL {
  constructor(
    thumbnail_url,
    fullsize_url) {
      this.thumbnail_url = thumbnail_url
      this.fullsize_url = fullsize_url
    }
}

/*
@dataclass
class AppDetail:
	detailed_description: str
	about_the_game: str
	short_description: str
	header_image_url: str
	developers: List[str]
	publishers: List[str]
	metacritic_score: int
	controller_support: bool
	genres: List[str]
	screenshot_urls: List[ScreenshotURL]
	background_image_url: str
*/
class AppDetail {
  constructor(
    detailed_description,
    about_the_game,
    short_description,
    header_image_url,
    developers,
    publishers,
    metacritic_score,
    controller_support,
    genres,
    screenshot_urls,
    background_image_url) {
      this.detailed_description = detailed_description
      this.about_the_game = about_the_game
      this.short_description = short_description
      this.header_image_url = header_image_url
      this.developers = developers
      this.publishers = publishers
      this.metacritic_score = metacritic_score
      this.controller_support = controller_support
      this.genres = genres
      this.screenshot_urls = screenshot_urls
      this.background_image_url = background_image_url
    }
}


// XXX I really don't like this being global - but it seems to be the only way to
// establish these connections before the first render call triggers
const socketContainer = new SocketContainer(endpoints);

class App extends Component {
  constructor() {
    super();
    this.state = {};
    for (const state of STATES.concat([GAMES])) {
      this.state[state] = [];
    }
    this.socketContainer = socketContainer;
    autoBind(this);
  }
  
  componentDidMount() {
    const sockets = Object.entries(socketContainer.get_sockets())
    for (const [state, sock] of sockets) {
      sock.onmessage = (message) => {
        const receivedMessage = JSON.parse(message.data);
        this.setState({
          [state]: receivedMessage
        });
      };

      sock.onopen = () => {
        console.log(`${state} open`);
      };
      sock.onclose = () => {
        console.log(`${state} close`);
      }
    }
  }
  
  render() {
    var debugBoardNeededStateData = {}
    for (const stateName of STATES) {
      debugBoardNeededStateData[stateName] = this.state[stateName];
    }

    let commandSocket;
    if (this.socketContainer) {
      commandSocket = this.socketContainer.get_socket(COMMAND)
    }

    const game_factory = new GameFactory()
    const games = this.state[GAMES].map(
      game_from_backend => game_factory.create_game(game_from_backend)
    );
    console.log(games)

    return (
      <Tabs renderActiveTabContentOnly={true}>
        <TabLink to="tab1" default>Games</TabLink>
        <TabLink to="tab2">User Input</TabLink>
        <TabLink to="tab3">Debug</TabLink>
      
        <TabContent for="tab1">
          <GameListView games={this.state[GAMES]}></GameListView>
        </TabContent>
        <TabContent for="tab2">"user input view"</TabContent>
        <TabContent for="tab3">
          <DebugBoard stateData={debugBoardNeededStateData} commandSocket={commandSocket}/>
        </TabContent>
      </Tabs>
    );
  }
}

export default App;
