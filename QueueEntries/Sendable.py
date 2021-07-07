from dataclasses import asdict, dataclass

@dataclass
class Sendable:
    game_name_on_disk: str

    def get_game_name_on_disk(self) -> str:
        return self.game_name_on_disk

@dataclass
class SteamSendable:
    game_name_on_disk: str
    game_name_from_steam: str

    def get_game_name_on_disk(self) -> str:
        return self.game_name_on_disk
    
    def get_game_name_from_steam(self) -> str:
        return self.game_name_from_steam