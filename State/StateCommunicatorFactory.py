from ObservedDataStructure.ObservedDataStructure import ObservedDataStructure
from typing import Set
from State.StateCommunicator import StateCommunicator

# type hints
from ObservedDataStructure.ObserverSocketHookupFactory import ObserverSocketHookupFactory

class StateCommunicatorFactory:
    def createStateCommunicator(self, observerSocketHookupFactory : ObserverSocketHookupFactory, states: Set[str], games_observable_data_structure: ObservedDataStructure):
        factoryMethod = observerSocketHookupFactory.hookUpObservableDataStructure

        # Dependency Injection makes testing State Tracker a heck of a lot easier
        connections = {}
        for state in states:
            connections[state] = factoryMethod(state)
        
        return StateCommunicator(connections, games_observable_data_structure)