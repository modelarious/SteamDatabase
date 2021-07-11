import Gallery from 'react-grid-gallery';
import React, { Component } from 'react';
const autoBind = require('auto-bind');

var IMAGES = [];
class GameListView extends Component {
    constructor(games) {
        super();
        this.state = {
            games: games['children']
        }
        autoBind(this);
    }
    // XXX can I move IMAGES into this class? can I access "this" GameListView in this function
    thumbnail_click_callback(idx) {
        console.log(IMAGES[idx].name)
    }
    render() {
        IMAGES = this.state.games.map(game =>
            ({
                thumbnail: game.app_detail.header_image_url,
                thumbnailWidth: 460,
                thumbnailHeight: 215
            })
        )
        console.log("render GameListView")
        console.log(this.state.games)
        return <div>
            <Gallery images={IMAGES} enableImageSelection={false} onClickThumbnail={this.thumbnail_click_callback}/>
        </div>
    }
}

export default GameListView;