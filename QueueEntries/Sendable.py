from dataclasses import dataclass

@dataclass
class Sendable:
    game_name_on_disk: str

    def get_game_name_on_disk(self) -> str:
        return self.game_name_on_disk