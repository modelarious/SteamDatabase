from State.States import STATES
from State.StateTracker import StateTracker

# type hints
from State.ObserverSocketHookupFactory import ObserverSocketHookupFactory

class StateTrackerFactory:
    def createStateTracker(self, observerSocketHookupFactory : ObserverSocketHookupFactory):
        factoryMethod = observerSocketHookupFactory.hookUpObservableDataStructure

        # Dependency Injection makes testing State Tracker a heck of a lot easier
        connections = {}
        for state in STATES:
            connections[state] = factoryMethod(state)
        
        return StateTracker(connections)