import Gallery from 'react-grid-gallery';
import React, { Component } from 'react';
const autoBind = require('auto-bind');

class GameListView extends Component {
    constructor() {
        super();
        this.games = [];
        autoBind(this);
    }
    thumbnail_click_callback(idx) {
        console.log(this.games[idx].game);
    }
    render() {
        this.games = this.props.games.map(game =>
            ({
                thumbnail: game.app_detail.header_image_url,
                thumbnailWidth: 460,
                thumbnailHeight: 215,
                game: game
            })
        );
        return <div>
            <Gallery images={this.games} enableImageSelection={false} onClickThumbnail={this.thumbnail_click_callback}/>
        </div>;
    }
}

export default GameListView;