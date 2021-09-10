const autoBind = require('auto-bind');

// https://stackoverflow.com/a/2466503
var byField = function (field) {
  return function (a, b) {
    if (typeof a[field] == "number") {
      return (b[field] - a[field]);
    } else {
      return ((a[field] < b[field]) ? -1 : ((a[field] > b[field]) ? 1 : 0));
    }
  };
};
export class ascendingSortingStrategy {
  constructor() {
    this._name = "Ascending";
    autoBind(this);
  }
  get_name() {
    return this._name;
  }
  sortGames(games, field) {
    const games_copy = JSON.parse(JSON.stringify(games));
    games_copy.sort(byField(field));
    return games_copy;
  }
}
