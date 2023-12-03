from QueueEntries.Sendable import SteamSendable
from dataclasses import asdict, dataclass
from typing import List
from ExternalDataFetchers.AppDetail import AppDetail


@dataclass
class Game(SteamSendable):
    game_name_on_disk: str
    game_name_from_steam: str
    steam_id: int
    path_on_harddrive: str
    avg_review_score: int
    user_defined_genres: List[str]
    app_detail: AppDetail
