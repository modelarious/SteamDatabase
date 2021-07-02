from QueueEntries.Sendable import SteamSendable
from dataclasses import asdict, dataclass
from typing import List
from ExternalDataFetchers.AppDetail import AppDetail

@dataclass
class Game(SteamSendable):
    steam_id: int
    game_name_on_disk: str
    path_on_harddrive: str
    game_name_from_steam: str
    avg_review_score: int
    user_defined_genres: List[str]
    app_detail : AppDetail
    
    def to_dict(self):
        return asdict(self)

