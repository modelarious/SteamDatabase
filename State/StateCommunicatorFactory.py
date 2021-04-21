from State.States import STATES
from State.StateCommunicator import StateCommunicator

# type hints
from State.ObserverSocketHookupFactory import ObserverSocketHookupFactory

class StateCommunicatorFactory:
    def createStateCommunicator(self, observerSocketHookupFactory : ObserverSocketHookupFactory):
        factoryMethod = observerSocketHookupFactory.hookUpObservableDataStructure

        # Dependency Injection makes testing State Tracker a heck of a lot easier
        connections = {}
        for state in STATES:
            connections[state] = factoryMethod(state)
        
        return StateCommunicator(connections)