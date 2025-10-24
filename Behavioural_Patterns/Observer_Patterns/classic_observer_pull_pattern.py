from typing import Any, Type, Optional, List
from abc import ABC, ABCMeta, abstractmethod
from threading import Lock
from enum import Enum


# States: (str enum)
class State(str, Enum):
    STATE_A = "State A Activated..."
    STATE_B = "State B Activated..."
    STATE_C = "State C Activated..."


# Subject (Interface)
class PullSubject(ABC):

    @abstractmethod
    def attach(self, observer: "ObserverPull") -> None:
        pass

    @abstractmethod
    def detach(self, observer: "ObserverPull") -> None:
        pass

    @abstractmethod
    def _notify(self):
        pass

    @abstractmethod
    def set_state(self, state: State) -> None:
        pass

    @abstractmethod
    def get_state(self) -> State:
        pass


# Concrete Subject
class ConcreteSubjectPull(PullSubject):
    """Subject Or Publisher: Notifies Observers of State Changes and allows them to react as desired."""

    def __init__(self) -> None:
        # use a set for better Big O Time Complexity
        self._observers: set[ObserverPull] = set() 
        self._state: State = State.STATE_A

    def attach(self, observer: "ObserverPull") -> None:
        """registers an Observer to the Subject"""
        self._observers.add(observer)  # 0(1) - time complexty

    def detach(self, observer: "ObserverPull") -> None:
        """Unregisters an Observer"""
        self._observers.discard(observer)   # 0(1) - time complexty

    def _notify(self) -> None:
        """Notifies all the registered observers of a state change. Via PULL Model"""
        for observer in self._observers:
            observer.update(self)

    def set_state(self, state: State) -> None:
        """Changes the state and Notifies the Observers."""
        self._state = state
        print(
            f"\nSubject: {self.__class__.__qualname__} is PULLING state to {self._state}"
        )
        self._notify()  # coupled to _notify()

    def get_state(self) -> State:
        """returns the current state of the Subject."""
        return self._state


# Observer (Interface)
class ObserverPull(ABC):

    @abstractmethod
    def update(self, subject: PullSubject) -> None:
        pass


# Concrete Observers
class ConcreteObserverPull(ObserverPull):
    """Observer or Subscriber: reacts to state change with behavioural logic."""

    def update(self, subject: PullSubject) -> None:
        """Uses Method from the Subject to Pull the changed State from the Subject."""
        state = subject.get_state()  # pulls state from the subject
        print(f"Class: {self.__class__.__qualname__}: {state.value}")


class ConcreteObserverPullB(ObserverPull):
    """Observer or Subscriber: reacts to state change with behavioural logic."""

    def update(self, subject: PullSubject) -> None:
        """Uses Method from the Subject to Pull the changed State from the Subject."""
        state = subject.get_state()  # pulls state from the subject
        print(f"Class: {self.__class__.__qualname__}: {state.value}")


class ConcreteObserverPullC(ObserverPull):
    """Observer or Subscriber: reacts to state change with behavioural logic."""

    def update(self, subject: PullSubject) -> None:
        """Uses Method from the Subject to Pull the changed State from the Subject."""
        state = subject.get_state()  # pulls state from the subject
        print(f"Class: {self.__class__.__qualname__}: {state.value}")


# Main --- User Facing Code ---
def main():

    # initialize Subject
    pull_subject = ConcreteSubjectPull()

    # Initialize Observers
    concrete_observer_pull_a = ConcreteObserverPull()
    concrete_observer_pull_b = ConcreteObserverPullB()
    concrete_observer_pull_c = ConcreteObserverPullC()

    pull_subject.attach(concrete_observer_pull_a)
    pull_subject.attach(concrete_observer_pull_b)
    pull_subject.attach(concrete_observer_pull_c)

    pull_subject.set_state(State.STATE_C)
    pull_subject.set_state(State.STATE_B)


if __name__ == "__main__":
    main()
