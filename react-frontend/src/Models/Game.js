/*
@dataclass
class Game(SteamSendable):
    game_name_on_disk: str
    game_name_from_steam: str
    steam_id: int
    path_on_harddrive: str
    avg_review_score: int
    user_defined_genres: List[str]
    app_detail : AppDetail
*/
export default class Game {
    constructor(
      game_name_on_disk,
      game_name_from_steam,
      steam_id,
      path_on_harddrive,
      avg_review_score,
      user_defined_genres,
      app_detail) {
        this.game_name_on_disk = game_name_on_disk
        this.game_name_from_steam = game_name_from_steam
        this.steam_id = steam_id
        this.path_on_harddrive = path_on_harddrive
        this.avg_review_score = avg_review_score
        this.user_defined_genres = user_defined_genres
        this.app_detail = app_detail
    }
}