import Gallery from 'react-grid-gallery';
import React, { Component } from 'react';
const autoBind = require('auto-bind');

var IMAGES = [];
function thumbnail_click_callback(idx) {
    console.log(IMAGES[idx].game)
}
function GameListView(props) {
    console.log(props.games)
    IMAGES = props.games.map(game =>
        ({
            thumbnail: game.app_detail.header_image_url,
            thumbnailWidth: 460,
            thumbnailHeight: 215,
            game:game
        })
    )
    console.log("render GameListView")
    return <div>
        <Gallery images={IMAGES} enableImageSelection={false} onClickThumbnail={thumbnail_click_callback}/>
    </div>
}

export default GameListView;