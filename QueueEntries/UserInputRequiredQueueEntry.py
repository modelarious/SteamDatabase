from QueueEntries.Sendable import Sendable
from dataclasses import dataclass
from typing import List
from QueueEntries.PossibleMatchQueueEntry import PossibleMatchQueueEntry

@dataclass
class UserInputRequiredQueueEntry(Sendable):
    game_name_on_disk: str
    possible_matches_list: List[PossibleMatchQueueEntry]
    
    def get_possible_matches_list(self):
        return self.possible_matches_list
