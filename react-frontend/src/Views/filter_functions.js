/* retrieval functions */
export function retrieve_name(game) {
    return game.game_name_from_steam;
}
export function retrieve_review_score(game) {
    return game.avg_review_score;
}
export function retrieve_genres(game) {
    return game.user_defined_genres;
}
export function retrieve_controller_support(game) {
    return game.app_detail.controller_support;
}


/* comparison functions */
export function string_includes(str, subStr) {
    return str.toLowerCase().includes(subStr.toLowerCase());
}
export function all_genres_apply_to_game(game_genre_tags, filter_genre_tags) {
    const intersection = game_genre_tags.filter(tag => filter_genre_tags.includes(tag));
    return intersection.length === filter_genre_tags.length;
}
export function exists_in_boolean_list(game_bool, filter_bool_list) {
    return filter_bool_list.includes(game_bool);
}

/* numerical functions */
export function greater_than(num, filter_num) {
    return parseInt(num) > parseInt(filter_num);
}
export function greater_than_or_equal_to(num, filter_num) {
    return parseInt(num) >= parseInt(filter_num);
}
export function less_than(num, filter_num) {
    return parseInt(num) < parseInt(filter_num);
}
export function less_than_or_equal_to(num, filter_num) {
    return parseInt(num) <= parseInt(filter_num);
}
export function equal(num, filter_num) {
    return parseInt(num) === parseInt(filter_num);
}
