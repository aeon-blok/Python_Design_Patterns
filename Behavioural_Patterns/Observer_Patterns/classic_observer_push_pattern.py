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
class PushSubject(ABC):

    @abstractmethod
    def attach(self, observer: "ObserverPush") -> None:
        pass

    @abstractmethod
    def detach(self, observer: "ObserverPush") -> None:
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
class ConcreteSubjectPush(PushSubject):
    """Subject Or Publisher: Notifies Observers of State Changes and allows them to react as desired."""

    def __init__(self) -> None:
        self._observers: set[ObserverPush] = set()
        self._state: State = State.STATE_A

    def attach(self, observer: "ObserverPush") -> None:
        """registers an Observer to the Subject"""
        self._observers.add(observer)

    def detach(self, observer: "ObserverPush") -> None:
        """Unregisters an Observer"""
        self._observers.discard(observer)  # 0(1) - time complexty

    def _notify(self) -> None:
        """Notifies all the registered observers of a state change. Via PUSH Model"""
        for observer in self._observers:
            observer.update(self._state)

    def set_state(self, state: State) -> None:
        """Changes the state and Notifies the Observers."""
        self._state = state
        print(
            f"\nSubject: {self.__class__.__qualname__} is PUSHING state to {self._state}"
        )
        self._notify()  # coupled to _notify()

    def get_state(self) -> State:
        """returns the current state of the Subject."""
        return self._state


# Observer (Interface)
class ObserverPush(ABC):

    @abstractmethod
    def update(self, state: State) -> None:
        pass


# Concrete Observers
class ConcreteObserverPush(ObserverPush):
    """Observer or Subscriber: reacts to state change with behavioural logic."""

    def update(self, state: State) -> None:
        """Subject directly pushes the state to the Observers"""
        print(f"Class: {self.__class__.__qualname__}: {state.value}")


class ConcreteObserverPushB(ObserverPush):
    """Observer or Subscriber: reacts to state change with behavioural logic."""

    def update(self, state: State) -> None:
        """Subject directly pushes the state to the Observers"""
        print(f"Class: {self.__class__.__qualname__}: {state.value}")


class ConcreteObserverPushC(ObserverPush):
    """Observer or Subscriber: reacts to state change with behavioural logic."""

    def update(self, state: State) -> None:
        """Subject directly pushes the state to the Observers"""
        print(f"Class: {self.__class__.__qualname__}: {state.value}")


# Main --- User Facing Code ---


def main():

    # initialize Subject
    push_subject = ConcreteSubjectPush()

    # Initialize Observers
    concrete_observer_push_a = ConcreteObserverPush()
    concrete_observer_push_b = ConcreteObserverPushB()
    concrete_observer_push_c = ConcreteObserverPushC()

    # register observers with Subject
    push_subject.attach(concrete_observer_push_a)
    push_subject.attach(concrete_observer_push_b)
    push_subject.attach(concrete_observer_push_c)

    # change state of Subject.
    push_subject.set_state(State.STATE_B)
    push_subject.set_state(State.STATE_A)


if __name__ == "__main__":
    main()
