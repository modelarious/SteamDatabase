import unittest
from unittest.mock import patch, call, MagicMock
from State.ObservedDataStructure import ObservedDataStructure
from State.StateTracker import StateTracker

class SomeClass:
    def method(self, a, b, c, key='hello'):
        return 1





class ObservedDataStructureTest(unittest.TestCase):

    def test_socket_update_called_on_creation_with_blank_set(self):
        # integration test
        real = SomeClass() 
        real.method = MagicMock(name='method')


        real.method(3, 4, 5, key='value')
        real.method(4, 5, 7, key='vasdfasddfalue')
        print(real.method.mock_calls)


        stateTracker = StateTracker()
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