import unittest
from unittest.mock import patch, call
from Server.SocketWrapper import SocketWrapper
from State.ObservedDataStructure import ObservedDataStructure

class ObservedDataStructureTest(unittest.TestCase):

    def test_socket_update_called_on_creation_with_blank_set(self):
        with patch.object(SocketWrapper, 'send_message', return_value=None) as mock_socket_send_message:
            socketWrapper = SocketWrapper(None, None)
            observedDataStructure = ObservedDataStructure(socketWrapper)

        mock_socket_send_message.assert_called_once_with(set())

    def test_socket_update_called_on_add_to_observed_data_structure(self):
        valueToAdd = 1
        with patch.object(SocketWrapper, 'send_message', return_value=None) as mock_socket_send_message:
            socketWrapper = SocketWrapper(None, None)
            observedDataStructure = ObservedDataStructure(socketWrapper)
            observedDataStructure.add(valueToAdd)
        
        calls = [
            call(set()), 
            call(set([valueToAdd]))
        ]
        mock_socket_send_message.assert_has_calls(calls)

    def test_socket_update_called_on_remove_from_observed_data_structure(self):
        valueToAdd = 1
        with patch.object(SocketWrapper, 'send_message', return_value=None) as mock_socket_send_message:
            socketWrapper = SocketWrapper(None, None)
            observedDataStructure = ObservedDataStructure(socketWrapper)
            observedDataStructure.add(valueToAdd)
            observedDataStructure.remove(valueToAdd)

        calls = [
            call(set()), 
            call(set([valueToAdd])),
            call(set()) 
        ]
        mock_socket_send_message.assert_has_calls(calls)

    def test_socket_update_called_on_add_by_tag_and_remove_by_tag(self):
        valueToAdd = 1
        keyToUse = "test key"
        with patch.object(SocketWrapper, 'send_message', return_value=None) as mock_socket_send_message:
            socketWrapper = SocketWrapper(None, None)
            observedDataStructure = ObservedDataStructure(socketWrapper)
            observedDataStructure.addByTag(keyToUse, valueToAdd)
            observedDataStructure.removeByTag(keyToUse)

        calls = [
            call(set()), 
            call(set([valueToAdd])),
            call(set()) 
        ]
        mock_socket_send_message.assert_has_calls(calls)

if __name__ == '__main__':
    unittest.main()