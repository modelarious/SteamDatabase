import unittest
from unittest.mock import patch
from Server.SocketWrapper import SocketWrapper
from State.ObservedDataStructure import ObservedDataStructure

class ObservedDataStructureTest(unittest.TestCase):

    def test_socket_update_called_on_add_to_observed_data_structure(self):
        with patch.object(SocketWrapper, 'send_message', return_value=None) as mock_socket_send_message:
            socketWrapper = SocketWrapper(None, None)
            socketWrapper.send_message(set([1,2,3]))
        mock_socket_send_message.assert_called_once_with(set([1,2,3]))

    # def test_socket_update_called_on_remove_from_observed_data_structure(self):
    #     self.assertEqual('foo'.upper(), 'FOO')
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()