import React, { Component } from 'react';
import Dropdown from 'react-dropdown';
import { ascendingSortingStrategy } from './Strategies/ascendingSortingStrategy';

const autoBind = require('auto-bind');

const ascendingStrategy = new ascendingSortingStrategy();
const sortingStrategies = [
  ascendingStrategy
];

let sortingStrategiesIndex = {}
for (const strategy of sortingStrategies) {
  sortingStrategiesIndex[strategy.get_name()] = strategy;
}
const sortingStrategyOptions = sortingStrategies.map(
  strat => strat.get_name()
)
const defaultSortStrategyOption = ascendingStrategy.get_name();

const sortingFieldsIndex = {
  "Steam Game Title": "game_name_from_steam",
  "Steam Average Review Score": "avg_review_score",
}

const sortingFieldOptions = Object.keys(sortingFieldsIndex)
const defaultSortFieldOption = sortingFieldOptions[0];

export class Sorter extends Component {
  constructor(onUpdate) {
    super();
    this.sortingField = sortingFieldsIndex[defaultSortFieldOption];
    this.sortingStrategy = sortingStrategiesIndex[defaultSortStrategyOption];
    this.onUpdate = onUpdate;
    autoBind(this);
  }

  _onSelectSortStrategy(sortStrategy) {
    const sortingStrategy = sortStrategy.value;
    this.sortingStrategy = sortingStrategiesIndex[sortingStrategy];
    this.onUpdate();
  }

  _onSelectSortField(sortField) {
    const sortingField = sortField.value;
    this.sortingField = sortingFieldsIndex[sortingField];
    this.onUpdate();
  }

  getSortedValues(games) {
    console.log(`sorting by ${this.sortingField}, using ${this.sortingStrategy.get_name()} strategy`);
    return this.sortingStrategy.sortGames(games, this.sortingField);
  }

  render() {
    const style = {
      display: 'flex',
      justifyContent: 'start',
      paddingLeft : '20px'
    };

    return <div style={style}>
      <text>Sort on</text>
      <Dropdown options={sortingFieldOptions} onChange={this._onSelectSortField} value={defaultSortFieldOption} placeholder="Sort Type" />
      <text>field in</text>
      <Dropdown options={sortingStrategyOptions} onChange={this._onSelectSortStrategy} value={defaultSortStrategyOption} placeholder="Sort Strategy" />
      <text>order</text>
    </div>;
  }
}
