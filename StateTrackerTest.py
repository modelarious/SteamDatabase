import unittest
from unittest.mock import call, MagicMock
from ObservedDataStructure.ObservedDataStructure import ObservedDataStructure
from State.StateCommunicator import StateCommunicator
from State.States import STATES, UPCOMING_STATE, FINDING_NAME_ACTIVE_STATE, AWAITING_USER_STATE, QUEUED_FOR_INFO_RETRIEVAL_STATE, INFO_RETRIEVAL_ACTIVE_STATE, STORED
from Server.SocketWrapper import SocketWrapper
from QueueEntries.PossibleMatchQueueEntry import PossibleMatchQueueEntry
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from GameModel import Game

gameTitleOnDisk = "Hello, I'm a game title"
possibleTitleMatch1 = "Hello, I'm a game title (tm)"
possibleTitleMatch2 = "Hello, I'm a game title 2"

# factories
def create_game():
    return Game(
        steam_id = "122999", 
        name_on_harddrive = gameTitleOnDisk, 
        path_on_harddrive = "hello", 
        name_on_steam = "hi there", 
        avg_review_score = 9.4,
        user_defined_genres = ['genre1', 'genre2']
    )

def create_match_queue_entry():
    return MatchQueueEntry("hello", gameTitleOnDisk, "13447289")

def create_user_input_required_queue_entry():
    possibleMatch1 = PossibleMatchQueueEntry(possibleTitleMatch1, "title 1", 0.91)
    possibleMatch2 = PossibleMatchQueueEntry(possibleTitleMatch2, "title 2", 0.98)
    possibleMatches = [
        possibleMatch1, 
        possibleMatch2
    ]
    return UserInputRequiredQueueEntry(gameTitleOnDisk, possibleMatches)

# integration test
class StateCommunicatorTest(unittest.TestCase):
    def setUp(self):
        
        self.observedDataStructures = {}
        for state in STATES:
            # could create a seam by mocking ObservedDataStructure, but I care more about
            # if the data is being sent through the socket when I use the StateCommunicator. This
            # way I can check what is going to be sent from the sockets to the front end.
            mockSocketWrapper = SocketWrapper(None, state)
            mockSocketWrapper.send_message = MagicMock(name=state + " socketWrapperSendMessageMock")

            self.observedDataStructures[state] = ObservedDataStructure(mockSocketWrapper)
    
    def get_sent_messages_mock(self, state):
        return self.observedDataStructures[state].socketToUpdate.send_message
    
    # should be a blank call on creation, then one call showing that a value has been added
    def assert_correct_call_structure_after_adding(self, expectedCallValue, state):
        sentMessageMock = self.get_sent_messages_mock(state)
        calls = [
            call([]), 
            call([expectedCallValue])
        ]
        sentMessageMock.assert_has_calls(calls)
        assert(len(sentMessageMock.mock_calls) == 2)
    
    def assert_correct_calls_after_moving_to_next_state(self, expectedCallValue, state):
        sentMessageMock = self.get_sent_messages_mock(state)

        calls = [
            call([]), 
            call([expectedCallValue]),
            call([])
        ]
        sentMessageMock.assert_has_calls(calls)
        assert(len(sentMessageMock.mock_calls) == 3)
    
    # several imperfect matches found - ask user for input
    def test_partial_match_flow(self):
        stateCommunicator = StateCommunicator(self.observedDataStructures)

        # set to upcoming state
        stateCommunicator.setUpcomingState(gameTitleOnDisk)
        self.assert_correct_call_structure_after_adding(gameTitleOnDisk, UPCOMING_STATE)

        # move to finding name active state
        stateCommunicator.setFindingNameActiveState(gameTitleOnDisk)
        self.assert_correct_calls_after_moving_to_next_state(gameTitleOnDisk, UPCOMING_STATE)
        self.assert_correct_call_structure_after_adding(gameTitleOnDisk, FINDING_NAME_ACTIVE_STATE)
        
        # move to input required because multiple titles match closely but none exactly
        userInputRequiredQueueEntry = create_user_input_required_queue_entry()
        stateCommunicator.setAwaitingUserInputState(userInputRequiredQueueEntry)
        self.assert_correct_calls_after_moving_to_next_state(gameTitleOnDisk, FINDING_NAME_ACTIVE_STATE)
        self.assert_correct_call_structure_after_adding(userInputRequiredQueueEntry.to_dict(), AWAITING_USER_STATE)

        # user selected an entry and we continue with processing
        matchQueueEntry = create_match_queue_entry()
        stateCommunicator.setQueuedForInfoRetrievalState(matchQueueEntry)
        self.assert_correct_calls_after_moving_to_next_state(userInputRequiredQueueEntry.to_dict(), AWAITING_USER_STATE)
        self.assert_correct_call_structure_after_adding(matchQueueEntry.to_dict(), QUEUED_FOR_INFO_RETRIEVAL_STATE)

        stateCommunicator.setInfoRetrievalActiveState(matchQueueEntry)
        self.assert_correct_calls_after_moving_to_next_state(matchQueueEntry.to_dict(), QUEUED_FOR_INFO_RETRIEVAL_STATE)
        self.assert_correct_call_structure_after_adding(matchQueueEntry.to_dict(), INFO_RETRIEVAL_ACTIVE_STATE)

        # persist the result 
        game = create_game()
        stateCommunicator.setStoredState(game)
        self.assert_correct_calls_after_moving_to_next_state(matchQueueEntry.to_dict(), INFO_RETRIEVAL_ACTIVE_STATE)
        self.assert_correct_call_structure_after_adding(game.to_dict(), STORED)
    
    # this one skips the phase where it requires user input
    def test_perfect_match_flow(self):
        stateCommunicator = StateCommunicator(self.observedDataStructures)

        # set to upcoming state
        stateCommunicator.setUpcomingState(gameTitleOnDisk)
        self.assert_correct_call_structure_after_adding(gameTitleOnDisk, UPCOMING_STATE)

        # move to finding name active state
        stateCommunicator.setFindingNameActiveState(gameTitleOnDisk)
        self.assert_correct_calls_after_moving_to_next_state(gameTitleOnDisk, UPCOMING_STATE)
        self.assert_correct_call_structure_after_adding(gameTitleOnDisk, FINDING_NAME_ACTIVE_STATE)
        
        # perfect match found - move straight to retrieving info
        matchQueueEntry = create_match_queue_entry()
        stateCommunicator.setQueuedForInfoRetrievalState(matchQueueEntry)
        self.assert_correct_calls_after_moving_to_next_state(gameTitleOnDisk, FINDING_NAME_ACTIVE_STATE)
        self.assert_correct_call_structure_after_adding(matchQueueEntry.to_dict(), QUEUED_FOR_INFO_RETRIEVAL_STATE)

        stateCommunicator.setInfoRetrievalActiveState(matchQueueEntry)
        self.assert_correct_calls_after_moving_to_next_state(matchQueueEntry.to_dict(), QUEUED_FOR_INFO_RETRIEVAL_STATE)
        self.assert_correct_call_structure_after_adding(matchQueueEntry.to_dict(), INFO_RETRIEVAL_ACTIVE_STATE)

        # persist the result 
        game = create_game()
        stateCommunicator.setStoredState(game)
        self.assert_correct_calls_after_moving_to_next_state(matchQueueEntry.to_dict(), INFO_RETRIEVAL_ACTIVE_STATE)
        self.assert_correct_call_structure_after_adding(game.to_dict(), STORED)

if __name__ == '__main__':
    unittest.main()


    