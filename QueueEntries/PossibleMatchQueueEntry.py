from QueueEntries.MatchQueueEntry import MatchQueueEntry
from dataclasses import dataclass

@dataclass
class PossibleMatchQueueEntry:
    steam_name: str
    steam_id_number: int
    match_score: float
    
    def get_match_score(self) -> float:
        return self.match_score
    
    def get_steam_name(self) -> str:
        return self.steam_name

    def convert_to_match_queue_entry(self, game_name_on_disk: str) -> MatchQueueEntry:
        return MatchQueueEntry(game_name_on_disk, self.steam_name, self.steam_id_number)
