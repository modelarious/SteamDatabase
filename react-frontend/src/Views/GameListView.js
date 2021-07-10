import Gallery from 'react-grid-gallery';
import React, { Component } from 'react';

  
  
// expecting to receive:
/*
{
commandSocket: A Socket that can be written to,
stateData: {
    [STATE_CONSTANT] : [array of objects currently in this state],
    [STATE_CONSTANT_2] : [array of objects currently in this state],
    [STATE_CONSTANT_3] : [array of objects currently in this state],
    ...
}
}
*/


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


class GameListView extends Component {
    thumbnail_click_callback(idx) {
        console.log(IMAGES[idx].name)
    }
    render() {
        return <div>
            <Gallery images={IMAGES} enableImageSelection={false} onClickThumbnail={this.thumbnail_click_callback}/>
        </div>
    }
}

export default GameListView;