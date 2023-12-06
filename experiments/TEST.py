from dataclasses import dataclass
import inspect


@dataclass
class Sendable:
    game_name_on_disk: str

    def get_game_name_on_disk(self) -> str:
        return self.game_name_on_disk


class InternalStateTracker:
    def __init__(self):
        self.previousStateTracker = {}

    def track(self, sendable: Sendable):
        game_on_disk = sendable.get_game_name_on_disk()
        print(self._determine_function_name())
        self.previousStateTracker[game_on_disk] = "farts"  # XXX

    def remove(self, sendable: Sendable):
        game_on_disk = sendable.get_game_name_on_disk()
        print(self._determine_function_name())
        del self.previousStateTracker[game_on_disk]

    def get(self, sendable: Sendable):
        game_on_disk = sendable.get_game_name_on_disk()
        return self.previousStateTracker[game_on_disk]

    def _determine_function_name(self):
        return inspect.stack()[1][3]


x = InternalStateTracker()
sendable = Sendable("HELLO")

x.track(sendable)
x.remove(sendable)

print("hello")
