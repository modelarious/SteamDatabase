import unittest
from unittest.mock import patch, call, MagicMock
from State.ObservedDataStructure import ObservedDataStructure
from State.StateTracker import StateTracker
from State.States import STATES, UPCOMING_STATE, FINDING_NAME_ACTIVE_STATE
from Server.SocketWrapper import SocketWrapper
from QueueEntries.PossibleMatchQueueEntry import PossibleMatchQueueEntry
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry

class SomeClass:
    def method(self, a, b, c, key='hello'):
        return 1





class ObservedDataStructureTest(unittest.TestCase):

    def get_sent_messages_mock(self, observedDataStructures, state):
        return observedDataStructures[state].socketToUpdate.send_message

        # .assert_called_once()

    def test_have_a_good_name(self):
        # integration test
        observedDataStructures = {}
        for state in STATES:
            # could create a seam by mocking ObservedDataStructure, but I care more about
            # if the data is being sent through the socket when I use the StateTracker. This
            # way I can check what is going to be sent from the sockets to the front end.
            mockSocketWrapper = SocketWrapper(None, state)
            mockSocketWrapper.send_message = MagicMock(name=state + " socketWrapperSendMessageMock")

            observedDataStructures[state] = ObservedDataStructure(mockSocketWrapper)


        gameTitle = "Hello, I'm a game title"
        possibleTitleMatch1 = "Hello, I'm a game title (tm)"
        possibleTitleMatch2 = "Hello, I'm a game title 2"


        stateTracker = StateTracker(observedDataStructures)
        stateTracker.setUpcomingState(gameTitle)
        upcomingSentMessagesMock = self.get_sent_messages_mock(observedDataStructures, UPCOMING_STATE)
        calls = [
            call(set()), 
            call(set([gameTitle]))
        ]
        upcomingSentMessagesMock.assert_has_calls(calls)

        stateTracker.setFindingNameActiveState(gameTitle)
        print(self.get_sent_messages_mock(observedDataStructures, UPCOMING_STATE))
        print(self.get_sent_messages_mock(observedDataStructures, FINDING_NAME_ACTIVE_STATE))


        possibleMatch1 = PossibleMatchQueueEntry(possibleTitleMatch1, "", 0.91)
        possibleMatch2 = PossibleMatchQueueEntry(possibleTitleMatch2, "", 0.98)
        possibleMatches = [
            possibleMatch1, 
            possibleMatch2
        ]
        userInputRequiredQueueEntry = UserInputRequiredQueueEntry(gameTitle, possibleMatches)
        stateTracker.setAwaitingUserInputState(userInputRequiredQueueEntry)

    # def test_socket_update_called_on_add_to_observed_data_structure(self):
    #     valueToAdd = 1
    #     with patch.object(StateTracker, 'send_message', return_value=None) as mock_socket_send_message:
    #         socketWrapper = SocketWrapper(None, None)
    #         observedDataStructure = ObservedDataStructure(socketWrapper)
    #         observedDataStructure.add(valueToAdd)
        
    #     calls = [
    #         call(set()), 
    #         call(set([valueToAdd]))
    #     ]
    #     mock_socket_send_message.assert_has_calls(calls)

    # def test_socket_update_called_on_remove_from_observed_data_structure(self):
    #     valueToAdd = 1
    #     with patch.object(SocketWrapper, 'send_message', return_value=None) as mock_socket_send_message:
    #         socketWrapper = SocketWrapper(None, None)
    #         observedDataStructure = ObservedDataStructure(socketWrapper)
    #         observedDataStructure.add(valueToAdd)
    #         observedDataStructure.remove(valueToAdd)

    #     calls = [
    #         call(set()), 
    #         call(set([valueToAdd])),
    #         call(set()) 
    #     ]
    #     mock_socket_send_message.assert_has_calls(calls)

    # def test_socket_update_called_on_add_by_tag_and_remove_by_tag(self):
    #     valueToAdd = 1
    #     keyToUse = "test key"
    #     with patch.object(SocketWrapper, 'send_message', return_value=None) as mock_socket_send_message:
    #         socketWrapper = SocketWrapper(None, None)
    #         observedDataStructure = ObservedDataStructure(socketWrapper)
    #         observedDataStructure.addByTag(keyToUse, valueToAdd)
    #         observedDataStructure.removeByTag(keyToUse)

    #     calls = [
    #         call(set()), 
    #         call(set([valueToAdd])),
    #         call(set()) 
    #     ]
    #     mock_socket_send_message.assert_has_calls(calls)

if __name__ == '__main__':
    unittest.main()