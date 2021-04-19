import unittest
from unittest.mock import call, MagicMock
from State.ObservedDataStructure import ObservedDataStructure
from State.StateTracker import StateTracker
from State.States import STATES, UPCOMING_STATE, FINDING_NAME_ACTIVE_STATE, AWAITING_USER_STATE
from Server.SocketWrapper import SocketWrapper
from QueueEntries.PossibleMatchQueueEntry import PossibleMatchQueueEntry
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry


class ObservedDataStructureTest(unittest.TestCase):

    def get_sent_messages_mock(self, state):
        return self.observedDataStructures[state].socketToUpdate.send_message
    
    def assert_correct_call_structure_after_adding_to_upcoming(self, gameTitle):
        upcomingSentMessagesMock = self.get_sent_messages_mock(UPCOMING_STATE)
        calls = [
            call([]), 
            call([gameTitle])
        ]
        upcomingSentMessagesMock.assert_has_calls(calls)
        assert(len(upcomingSentMessagesMock.mock_calls) == 2)
    
    def assert_upcoming_had_correct_calls_after_moving_to_next_state(self, gameTitle):
        upcomingSentMessagesMock = self.get_sent_messages_mock(UPCOMING_STATE)

        calls = [
            call([]), 
            call([gameTitle]),
            call([])
        ]
        upcomingSentMessagesMock.assert_has_calls(calls)
        assert(len(upcomingSentMessagesMock.mock_calls) == 3)
    
    def assert_findingNameActive_correct_after_adding_to_findingNameActive(self, gameTitle):
        findingNameActiveStateMock = self.get_sent_messages_mock(FINDING_NAME_ACTIVE_STATE)
        calls = [
            call([]), 
            call([gameTitle])
        ]
        findingNameActiveStateMock.assert_has_calls(calls)
        assert(len(findingNameActiveStateMock.mock_calls) == 2)


    def test_have_a_good_name(self):
        # integration test
        self.observedDataStructures = {}
        for state in STATES:
            # could create a seam by mocking ObservedDataStructure, but I care more about
            # if the data is being sent through the socket when I use the StateTracker. This
            # way I can check what is going to be sent from the sockets to the front end.
            mockSocketWrapper = SocketWrapper(None, state)
            mockSocketWrapper.send_message = MagicMock(name=state + " socketWrapperSendMessageMock")

            self.observedDataStructures[state] = ObservedDataStructure(mockSocketWrapper)

        gameTitle = "Hello, I'm a game title"
        possibleTitleMatch1 = "Hello, I'm a game title (tm)"
        possibleTitleMatch2 = "Hello, I'm a game title 2"

        stateTracker = StateTracker(self.observedDataStructures)

        # set to upcoming state
        stateTracker.setUpcomingState(gameTitle)
        self.assert_correct_call_structure_after_adding_to_upcoming(gameTitle)

        # move to finding name active state
        stateTracker.setFindingNameActiveState(gameTitle)
        self.assert_upcoming_had_correct_calls_after_moving_to_next_state(gameTitle)
        self.assert_findingNameActive_correct_after_adding_to_findingNameActive(gameTitle)
        
        possibleMatch1 = PossibleMatchQueueEntry(possibleTitleMatch1, "", 0.91)
        possibleMatch2 = PossibleMatchQueueEntry(possibleTitleMatch2, "", 0.98)
        possibleMatches = [
            possibleMatch1, 
            possibleMatch2
        ]
        userInputRequiredQueueEntry = UserInputRequiredQueueEntry(gameTitle, possibleMatches)
        stateTracker.setAwaitingUserInputState(userInputRequiredQueueEntry)
        print(self.get_sent_messages_mock(FINDING_NAME_ACTIVE_STATE).mock_calls)
        print(self.get_sent_messages_mock(AWAITING_USER_STATE).mock_calls)


        # stateTracker.setInfoRetrievalActiveState()
        # stateTracker.setStoredState()

if __name__ == '__main__':
    unittest.main()