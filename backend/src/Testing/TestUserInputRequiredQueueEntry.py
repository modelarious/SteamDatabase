import unittest
from QueueEntries.PossibleMatchQueueEntry import PossibleMatchQueueEntry
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry

gameTitleOnDisk = "Hello, I'm a game title"
possibleTitleMatch1 = "Hello, I'm a game title (tm)"
possibleTitleMatch2 = "Hello, I'm a game title 2"


def create_user_input_required_queue_entry():
    possibleMatch1 = PossibleMatchQueueEntry(possibleTitleMatch1, "title 1", 0.91)
    possibleMatch2 = PossibleMatchQueueEntry(possibleTitleMatch2, "title 2", 0.98)
    possibleMatches = [possibleMatch1, possibleMatch2]
    return UserInputRequiredQueueEntry(gameTitleOnDisk, possibleMatches)


class UserInputRequiredQueueEntryTest(unittest.TestCase):
    def test_create(self):
        create_user_input_required_queue_entry()

    # was getting errors here originally because I was modifying self.__dict__ in the object
    # instead of self.__dict__.copy(). This modified the object itself which caused the second
    # call to toDict() to fail
    def test_transform_multiple(self):
        x = create_user_input_required_queue_entry()
        x.toDict()
        x.toDict()
        x.toDict()
        x.toDict()


if __name__ == "__main__":
    unittest.main()
