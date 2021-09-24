const autoBind = require('auto-bind');

export class filter {
    constructor(initial_value, filter_boolean_function, game_accessor_function) {
        this.filter_state = initial_value;
        this.filter_boolean_function = filter_boolean_function;
        this.game_accessor_function = game_accessor_function;
        autoBind(this);
    }

    update_filter_state(new_value) {
        this.filter_state = new_value;
    }

    update_filter_boolean_function(new_function) {
        this.filter_boolean_function = new_function;
    }

    _apply_to_game(game) {
        const field_value = this.game_accessor_function(game);
        return this.filter_boolean_function(field_value, this.filter_state);
    }

    apply(games) {
        return games.filter(game => this._apply_to_game(game));
    }
}
