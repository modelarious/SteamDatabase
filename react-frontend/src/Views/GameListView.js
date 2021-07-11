import Gallery from 'react-grid-gallery';
import React, { Component } from 'react';
const autoBind = require('auto-bind');


const IMAGES = [
{
    name: "doin ght",
    thumbnail: "https://cdn.akamai.steamstatic.com/steam/apps/522240/header.jpg?t=1584658980",
    thumbnailWidth: 460,
    thumbnailHeight: 215
},
{
    name: "doin ght",
    thumbnail: "https://cdn.akamai.steamstatic.com/steam/apps/656350/header.jpg?t=1618246992",
    thumbnailWidth: 460,
    thumbnailHeight: 215
},
{
    name: "doin ght",
    thumbnail: "https://cdn.akamai.steamstatic.com/steam/apps/427520/header.jpg?t=1620730652",
    thumbnailWidth: 460,
    thumbnailHeight: 215
},
];


class GameListView extends Component {
    constructor(games) {
        super();
        this.games = games;
        console.log(this.games)
        autoBind(this);
    }
    thumbnail_click_callback(idx) {
        console.log(IMAGES[idx].name)
    }
    render() {
        // const IMAGES = [
        //     {
        //         name: "doin ght",
        //         thumbnail: "https://cdn.akamai.steamstatic.com/steam/apps/522240/header.jpg?t=1584658980",
        //         thumbnailWidth: 460,
        //         thumbnailHeight: 215
        //     }
        // ]
        return <div>
            <Gallery images={IMAGES} enableImageSelection={false} onClickThumbnail={this.thumbnail_click_callback}/>
        </div>
    }
}

export default GameListView;