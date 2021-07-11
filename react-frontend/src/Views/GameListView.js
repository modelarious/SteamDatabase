import Gallery from 'react-grid-gallery';
import React, { Component } from 'react';
const autoBind = require('auto-bind');

class GameListView extends Component {
    constructor(props) {
        super();
        console.log("Construct GameListView");
        this.IMAGES = props.games.map(game =>
            ({
                thumbnail: game.app_detail.header_image_url,
                thumbnailWidth: 460,
                thumbnailHeight: 215,
                game: game
            })
        )
        autoBind(this);
    }
    thumbnail_click_callback(idx) {
        console.log(this.IMAGES[idx].game)
    }
    render() {
        console.log("Render GameListView");
        this.IMAGES = this.props.games.map(game =>
            ({
                thumbnail: game.app_detail.header_image_url,
                thumbnailWidth: 460,
                thumbnailHeight: 215,
                game: game
            })
        )
        return <div>
            <Gallery images={this.IMAGES} enableImageSelection={false} onClickThumbnail={this.thumbnail_click_callback}/>
        </div>
    }
 }

export default GameListView;