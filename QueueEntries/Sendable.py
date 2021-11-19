from dataclasses import dataclass

@dataclass
class Sendable:
    game_name_on_disk: str
    def get_game_name_on_disk(self) -> str:
        return self.game_name_on_disk

@dataclass
class ErrorSendable(Sendable):
    def __init__(self, sendable: Sendable, error_string: str):
        self.game_name_on_disk = sendable.get_game_name_on_disk()
        self.error_string = error_string

@dataclass
class SteamSendable(Sendable):
    game_name_on_disk: str
    game_name_from_steam: str
    def get_game_name_from_steam(self) -> str:
        return self.game_name_from_steam
