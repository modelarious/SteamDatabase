from QueueEntries.Sendable import SteamSendable
from dataclasses import dataclass

@dataclass
class MatchQueueEntry(SteamSendable):
    game_name_on_disk: str
    game_name_from_steam: str
    steam_id_number: int

    def get_game_name_from_steam(self):
        return self.game_name_from_steam
    
    def get_game_name_on_disk(self):
        return self.game_name_on_disk

    def get_steam_id_number(self):
        return self.steam_id_number
    
    def to_dict(self):
        return self.__dict__.copy()