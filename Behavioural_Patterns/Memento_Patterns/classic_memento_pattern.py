from collections.abc import Iterable
from typing import Any, Type, Optional, List
from abc import ABC, ABCMeta, abstractmethod
from threading import Lock
from enum import Enum
from dataclasses import dataclass
import copy
import inspect

"""Capture and externalize an object’s internal state so it can be restored later, without violating encapsulation."""

# Memento (Snapshot Object)
class iMemento(ABC):

    @abstractmethod
    def get_state(self) -> dict:
        pass


class Memento(iMemento):
    """Stores an In Memory Snapshot of all the attributes of the Originator"""

    def __init__(self, snapshot: dict) -> None:
        self.__snapshot = copy.deepcopy(snapshot)

    def get_state(self) -> dict:
        """returns the currently saved state inside Memento Object."""
        return self.__snapshot


# Originator (Target Object)
class iOriginator(ABC):
    """Interface for Originator - seperate into business logic and Memento Management"""

    # Business Logic
    @abstractmethod
    def dynamic_attributes(self, kwargs: dict) -> None:
        pass

    @abstractmethod
    def remove_attribute(self, key: str) -> None:
        pass

    @abstractmethod
    def add_attribute(self, key: str, value: Any, readonly: bool = False) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    # memento management
    @abstractmethod
    def save_memento(self) -> Memento:
        pass

    @abstractmethod
    def restore_memento(self, memento: Memento) -> None:
        pass


class Originator(iOriginator):
    """Originator Stores the Specific Data that we wish to save with the Memento. It Shuttles this data, to and from the Memento Object."""

    def _readonly_error(self, key):
        """"""
        if key in self.__dict__.get("_readonly", set()):
            raise AttributeError(f"{key}: is readonly. Permission Denied!")

    def _attribute_exists(self, key):
        """"""
        if key not in self.__dict__:
            raise AttributeError(
                f"{key}: Does not Exist! Available Attributes are: {self.__dict__.keys()}"
            )

    def __setattr__(self, key: str, value: Any) -> None:
        """Overrides setattr: readonly attributes are forbidden"""
        self._readonly_error(key)
        super().__setattr__(key, value)  # calls original setattr

    def __getattr__(self, key: str) -> Any:
        """Overrides getattr: Ensures key exists"""
        self._attribute_exists(key)
        return self.__dict__[key]

    def __dir__(self) -> Iterable[str]:
        """Overrides dir() to add dynamic attributes"""
        standard_attributes = list(super().__dir__())
        dynamic_attributes = [key for key in self.__dict__ if key != "_readonly"]
        return standard_attributes + dynamic_attributes

    def __init__(self, **kwargs) -> None:
        self.__dict__["_readonly"] = set()  # tracks readonly attributes per instance
        self.dynamic_attributes(kwargs)  # adds attributes automatically

    def dynamic_attributes(self, kwargs: dict) -> None:
        """Adds Kwargs to Instance Attributes automatically with logic for readonly attributes."""
        for k, v in kwargs.items():
            # add attribute to readonly set if ends with "_readonly"
            if k.endswith("_readonly"):
                self._readonly.add(k)  # type: ignore
            self.__dict__[k] = v

    def add_attribute(self, key: str, value: Any, readonly: bool = False) -> None:
        """Can Dynamically Add Attributes to the Object, with optional readonly logic"""
        if hasattr(self.__class__, key) or key in self.__dict__:
            raise AttributeError(f"Class Attribute Already Exists!")
        if readonly:
            self._readonly.add(key)  # type: ignore
        self.__dict__[key] = value

    def remove_attribute(self, key: str) -> None:
        """Dynamically removes an attribute from the object."""
        self._attribute_exists(key)
        self._readonly_error(key)
        self.__dict__.pop(key, None)

    def __str__(self) -> str:
        return f"Class: {self.__class__.__qualname__}\nAttributes: {', '.join(f'{k}: {v}' for k,v in self.__dict__.items())}"

    # Memento Logic
    def save_memento(self) -> Memento:
        """Deep copy all Originator attributes into Memento Snapshot."""
        return Memento(self.__dict__)

    def restore_memento(self, memento: Memento) -> None:
        previous_state = memento.get_state()
        self.__dict__.update(previous_state)


# Caretaker (History Manager)
class iCaretaker(ABC):
    pass


class Caretaker:
    """The Caretaker manages the history of Mementos (like an undo stack)."""

    def __init__(self, originator: Originator) -> None:
        self._originator = originator
        
        self._undo_stack: List[Memento] = []
        self._redo_stack: List[Memento] = []

    def save(self):
        """Asks the Originator to create a Memento and saves it in a list."""
        print(f"Saving Snapshot of Current State! Undo and Redo are Reset!")
        # coupled to Originator
        self._undo_stack.append(self._originator.save_memento())
        self._redo_stack.clear()  # previous redo history is no longer valid.

    def undo(self):
        """reverts Originator state to previous snapshot (memento object)"""
        if not self._undo_stack:
            raise IndexError(f"No Saved States to Undo")
        # Add item to redo stack.
        self._redo_stack.append(self._originator.save_memento())
        previous_state = self._undo_stack.pop()
        print("...reverted to previous state")
        self._originator.restore_memento(previous_state)  # coupled to Originator

    def redo(self):
        """reverts Originator state to past state that was previously applied (snapshot via memento)"""
        if not self._redo_stack:
            raise IndexError(f"No Saved States to redo")
        # Add item to Undo Stack
        self._undo_stack.append(self._originator.save_memento())
        previous_state = self._redo_stack.pop()
        print(f"...negated previous state reversion")
        self._originator.restore_memento(previous_state)


# Main --- Client Facing Code ---
def main():
    pass




if __name__ == "__main__":
    main()
