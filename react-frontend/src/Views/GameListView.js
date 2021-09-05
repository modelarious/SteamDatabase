import React, { Component } from 'react';
import { BrowserRouter, Switch, Route } from "react-router-dom";
import GameView from "./GameView";
import { Home } from './Home';
// import { Dropdown } from 'semantic-ui-react'
// import { DropdownExampleInline } from './garbage2';
// import { PageTransition } from "@steveeeie/react-page-transition";




// const friendOptions = [
//   {
//     key: 'Jenny Hess',
//     text: 'Jenny Hess',
//     value: 'Jenny Hess',
//     image: { avatar: true, src: '/images/avatar/small/jenny.jpg' },
//   },
//   {
//     key: 'Elliot Fu',
//     text: 'Elliot Fu',
//     value: 'Elliot Fu',
//     image: { avatar: true, src: '/images/avatar/small/elliot.jpg' },
//   },
//   {
//     key: 'Stevie Feliciano',
//     text: 'Stevie Feliciano',
//     value: 'Stevie Feliciano',
//     image: { avatar: true, src: '/images/avatar/small/stevie.jpg' },
//   },
//   {
//     key: 'Christian',
//     text: 'Christian',
//     value: 'Christian',
//     image: { avatar: true, src: '/images/avatar/small/christian.jpg' },
//   },
// ]


// class DropdownExampleInline extends Component {
//   render() {
//     return <span>
//       Show me posts by{' '}
//         <Dropdown
//           inline
//           options={friendOptions}
//           defaultValue={friendOptions[0].value}
//         />
//     </span>
//   }
// };
import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';

const SortingDirectionOptions = [
  'Ascending', 'Descending'
];
const defaultSortDirectionOption = SortingDirectionOptions[0];

const SortingTypeOptions = [
  'Name', 'Rating'
];
const defaultSortTypeOption = SortingTypeOptions[0];


const autoBind = require('auto-bind');


class GameListView extends Component {
  constructor(props) {
    super();
    this.games = props.games;
    this.sortingType = defaultSortTypeOption;
    this.sortingDirection = defaultSortDirectionOption;
    autoBind(this);
  }

  scrollDistanceUpdate(currentPixelsFromTop) {
    this.pixelsFromTop = currentPixelsFromTop;
  }

  _onSelectSortDirection(sortDirection) {
    this.sortingDirection = sortDirection.value;
  }

  _onSelectSortType(sortType) {
    this.sortingType = sortType.value;
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
                    <Dropdown options={SortingDirectionOptions} onChange={this._onSelectSortDirection} value={defaultSortDirectionOption} placeholder="Select an option" />
                    <Dropdown options={SortingTypeOptions} onChange={this._onSelectSortType} value={defaultSortTypeOption} placeholder="Select an option" />
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
