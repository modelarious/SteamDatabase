import React, { Component } from 'react';
import SocketContainer from "./SocketContainer.js";
import { STATES } from './States.js';
import {
  TabLink,
  Tabs,
  TabContent
} from 'react-tabs-redux';
import DebugBoard from './Views/DebugBoard';
import Gallery from 'react-grid-gallery';
const autoBind = require('auto-bind');
const COMMAND = "/command";
const GAMES = "/games";
const endpoints = STATES.concat([
  COMMAND,
  GAMES
]);

const IMAGES = [{
  name: "hello good sir",
  src: "https://c2.staticflickr.com/9/8817/28973449265_07e3aa5d2e_b.jpg",
  thumbnail: "https://c2.staticflickr.com/9/8817/28973449265_07e3aa5d2e_b.jpg",
  thumbnailWidth: 320,
  thumbnailHeight: 174,
  caption: "After Rain (Jeshu John - designerspics.com)"
},
{
  name: "how are you",
  src: "https://c2.staticflickr.com/9/8356/28897120681_3b2c0f43e0_b.jpg",
  thumbnail: "https://c2.staticflickr.com/9/8356/28897120681_3b2c0f43e0_n.jpg",
  thumbnailWidth: 320,
  thumbnailHeight: 212,
  tags: [{value: "Ocean", title: "Ocean"}, {value: "People", title: "People"}],
  caption: "Boats (Jeshu John - designerspics.com)"
},
{
  name: "doin ght",
  src: "https://c4.staticflickr.com/9/8887/28897124891_98c4fdd82b_b.jpg",
  thumbnail: "https://c4.staticflickr.com/9/8887/28897124891_98c4fdd82b_n.jpg",
  thumbnailWidth: 320,
  thumbnailHeight: 212
}];

// XXX I really don't like this being global - but it seems to be the only way to
// establish these connections before the first render call triggers
const socketContainer = new SocketContainer(endpoints);

class App extends Component {
  constructor() {
    super();
    this.state = {};
    for (const state of STATES) {
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

  thumbnail_click_callback(idx) {
    console.log(IMAGES[idx].name)
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

    return (
      <Tabs renderActiveTabContentOnly={true}>
        <TabLink to="tab1" default>Games</TabLink>
        <TabLink to="tab2">User Input</TabLink>
        <TabLink to="tab3">Debug</TabLink>
      
        <TabContent for="tab1">
          <Gallery images={IMAGES} enableImageSelection={false} onClickThumbnail={this.thumbnail_click_callback}/>
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
