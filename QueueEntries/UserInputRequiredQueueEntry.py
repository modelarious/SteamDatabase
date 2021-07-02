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
    
    def to_dict(self):
        props = self.__dict__.copy()
        # need to apply __dict__ to sub objects in the possible_matches_list
        props['possible_matches_list'] = [x.to_dict() for x in self.possible_matches_list]
    
        return props
