from dataclasses import asdict, dataclass
from typing import List
from ExternalDataFetchers.AppDetail import AppDetail

@dataclass
class Game:
    steam_id: int
    name_on_harddrive: str
    path_on_harddrive: str
    name_on_steam: str
    avg_review_score: int
    user_defined_genres: List[str]
    app_detail : AppDetail
    
    def to_dict(self):
        return asdict(self)

    
