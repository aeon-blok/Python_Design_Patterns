from threading import Lock
from enum import Enum
from dataclasses import dataclass, field
import copy
import inspect
from collections.abc import Iterable
from typing import Any, Type, Optional, List
from abc import ABC, ABCMeta, abstractmethod
import pickle
from pathlib import Path
from datetime import datetime

# pyright: reportGeneralTypeIssues=false

# Memento
class iMemento(ABC):

    @abstractmethod
    def get_snapshot(self) -> "iOriginator":
        pass


class Memento(iMemento):
    """receives a deep copy of an objects internal state. which it can provide on request"""
    def __init__(self, state) -> None:
        self._state = state

    def get_snapshot(self) -> "iOriginator":
        """returns a deep copy of the objects internal state."""
        return copy.deepcopy(self._state)


# Originator


class iOriginator(ABC):

    @abstractmethod
    def create_memento(self) -> iMemento:
        pass

    @abstractmethod
    def restore_memento(self, memento: iMemento) -> None:
        pass


class Readonly:
    """Marks attribute as readonly - its a wrapper - the actual functionality happens in the __setattr__"""
    def __init__(self, value):
        self._value = value


class Originator(iOriginator):
    """ Target Object that shares its internal state to the Memento. extra functionality for whatever the object is needed for..."""

    def __setattr__(self, key: str, value: Any) -> None:
        """Overrides setattr to Enforce READONLY attributes"""
        # STEP 1: if existing attribute: check if readonly - raise error
        if hasattr(self, "_readonly") and key in self.__readonly:
            raise AttributeError(f"{key}: is READ ONLY!")
        # STEP 2 is readonly wrapper detected - add to readonly set and store value
        if isinstance(value, Readonly): 
            self.__readonly.add(key)
            value = value._value    # stores the actual value
        # STEP 3: sets the attribute as normal
        object.__setattr__(self, key, value) 

    def __init__(self, caretaker: Optional['iCaretaker'] = None, **kwargs) -> None:
        # used for capturing changes in nested objects.
        self.__caretaker = caretaker # composed object reference to Caretaker
        self.__readonly = set() # stores readonly attributes (set by helper class)

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def caretaker(self):
        return self.__caretaker

    @caretaker.setter
    def caretaker(self, value):
        self.__caretaker = value

    def set_state(self, **kwargs):
        """Helper Method - that redefines attributes for the class dynamically."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        modified_attributes = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        description = f"Updated: {modified_attributes}"

        # automatically checkpoints after every change in state....
        if self.__caretaker:
            self.__caretaker.checkpoint(description=description)

    def delete_state(self, *args):
        """Helper Method - deletes attributes dynamically"""
        # expression - creates a dict of key and values for the arguments
        deleted_attributes = {key: getattr(self, key) for key in args if hasattr(self, key)}

        # delete attributes
        for key in deleted_attributes:
            delattr(self, key)

        string_del_attrs = ", ".join(f"{k}={v}" for k, v in deleted_attributes.items())
        # if there are deleted attributes - create decription
        description = (
            f"Deleted: {string_del_attrs}" if deleted_attributes else None
        )

        # automatically checkpoints after every change in state....
        if deleted_attributes and self.__caretaker:
            self.__caretaker.checkpoint(description=description)

    def __str__(self) -> str:
        """Information about the Attributes of the Current Object and any Nested Objects."""
        def recursive_collect_attrs(obj):
            """recursively parses nested structures and gets the attributes and displays them"""
            parts = []
            for key, value in obj.__dict__.items():
                # skip internal attributes and readonly attributes
                if key.startswith("_Originator__") or key == "_readonly":
                    continue
                # If the attribute is another Originator, show a short summary
                if isinstance(value, Originator):
                    parts.append(f"{key}=({recursive_collect_attrs(value)})")
                else:
                    parts.append(f"{key}={value}")
            return ", ".join(parts)
        return recursive_collect_attrs(self)

    # Memento Management
    def create_memento(self) -> iMemento:
        """Creates a Snapshot of the internal state of the object (its the whole object), that it sends to the Memento"""
        return Memento(copy.deepcopy(self))

    def restore_memento(self, memento: iMemento) -> None:
        """restores a previously saved snapshot of the internal state, and updates the current internal state to match. Handles nested objects"""

        def _recursive_restore(snapshot, target):
            # Replace all attributes with the snapshot attributes via deepcopy. needed for nested objects
            for key, value in snapshot.__dict__.items():
                # if originator object - calls function on it.
                if isinstance(value, iOriginator):
                    # ? checks existence and is Object. -applies recursive function
                    if hasattr(target, key) and isinstance(getattr(target, key), iOriginator):
                        recursive_restore(value, getattr(target, key)) 
                    else:
                        setattr(target, key, copy.deepcopy(value)) # set attribute via deepcopy
                else:
                    setattr(target, key, copy.deepcopy(value)) # set attribute via deepcopy

        self.__dict__.clear()  # Remove current attributes
        snapshot = memento.get_snapshot()  # retrieves memento
        _recursive_restore(snapshot, self) # runs recursive restore function

        # Replace all attributes with the snapshot attributes via deepcopy. needed for nested objects
        # for key, value in snapshot.__dict__.items():
        #     setattr(self, key, copy.deepcopy(value))


# Caretaker
class iCaretaker(ABC):

    @abstractmethod
    def checkpoint(self, description: Optional[str]) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    @abstractmethod
    def redo(self) -> None:
        pass

    @abstractmethod
    def save_to_disk(self, filename) -> Path:
        pass

    @abstractmethod
    def load_from_disk(self, filepath) -> None:
        pass


class Caretaker(iCaretaker):
    """Manages Memento Objects for the Originator, has Undo & Redo and Load and Save Functionality"""
    def __init__(self, originator: iOriginator, directory: str = "mementos") -> None:
        self._history: list[iMemento] = []  # database proxy
        # tracks current pos of history list, undo moves backwards, redo moves forwards
        # checkpoint moves to the end of the history list.
        self._current_pos = 0   

        self._labels: list[str] = []
        self._label_counter = 0

        self._directory = Path(directory)
        self._directory.mkdir(exist_ok=True)

        # Composed Originator Object
        self._originator = originator
        # attaches Caretaker instance to Originator
        self._originator.caretaker = self   # type: ignore
        self._history.append(self._originator.create_memento()) # create initial memento
        initial_label = self._generate_label("Initial State")
        self._labels.append(initial_label)


    def _generate_label(self, description: Optional[str] = None):
        """Automatically generates a label for memento objects (for history log.)"""
        self._label_counter += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        label = f"Memento: {self._label_counter:03d} {timestamp}"
        if description:
            label += f": {description}"
        return label

    def display_history_log(self):
        """Generates a log listing all the various memento objects."""
        print(f"\n--- History Log ---")
        for index, label in enumerate(self._labels):
            current_marker = (" <-- Current" if index == self._current_pos else "")
            print(f"{index + 1}: {label}{current_marker}")


    def checkpoint(self, description: Optional[str] = None):
        """creates a snapshot of the current state and updates history position"""
        memento = self._originator.create_memento() # create snapshot of current state
        self._history.append(memento)   # adds to history
        label = self._generate_label(description)   # adds auto generated label with optional user desc
        self._labels.append(label)  # adds to labels
        self._current_pos = len(self._history) -1 # moves counter to end of history list.

    def undo(self) -> None:
        """Undo Functionality - returns back to the last record checkpoint"""
        if self._current_pos == 0:
            raise ValueError(f"undo: nothing to undo...")

        self._current_pos -= 1  # current position goes back 1 step
        memento = self._history[self._current_pos]  # retreive memento from previous step
        self._originator.restore_memento(memento)   # revert state back to this memmento

    def redo(self) -> None:
        """redo functionality - returns back to last undo."""
        if self._current_pos >= len(self._history) - 1:
            raise ValueError(f"redo: at newest state already...")

        self._current_pos += 1  # increment current position counter
        memento = self._history[self._current_pos]  # retreive this memento
        self._originator.restore_memento(memento)   # revert state to this memento (forwards...)

    def save_to_disk(self, filename) -> Path:
        """Saves a Memento to disk as a pickle file."""
        filename = f"{filename}.pickle"
        label = self._generate_label(f"Saved to Disk: {filename}")
        self._labels.append(label)
        filepath = self._directory / filename

        memento = self._originator.create_memento() # create snapshot of current state
        self._history.append(memento)   # adds to history
        self._current_pos = len(self._history) -1 # moves counter to end of history list.

        # can encapsulate in try - except clause for retries etc...
        with open(filepath, "wb") as file:
            pickle.dump(memento, file)
        return filepath

    def load_from_disk(self, filepath) -> None:
        """Loads a Memento pickle file from disk"""
        if not filepath.is_file():
            raise ValueError (f"{filepath}: does not exist!")
        with open(filepath, "rb") as file:
            memento = pickle.load(file)
        self._originator.restore_memento(memento)  # Restores state from file
        self._history.append(memento)  # adds to history
        label = self._generate_label(f"Loaded from Disk: {filepath.name}")
        self._labels.append(label)
        self._current_pos = len(self._history) - 1 # moves counter to end of history list.


# Main
def main():

    def simple_originator_test():
        # Initialize Originator (our document)
        doc = Originator(title="My Document", content="Hello World!")

        # Initialize Caretaker
        caretaker = Caretaker(doc)

        # Initial State
        print("Initial State:", doc.title, doc.content)

        # Change content
        doc.content = "Hello OpenAI!" # does not work correctly. (not part of set_state() - its ok)
        doc.set_state(content="Hello OpenAI!")
        print("After edit 1:", doc.title, doc.content)

        # Change content again
        doc.set_state(content="Hello ChatGPT!")
        print("After edit 2:", doc.title, doc.content)

        # Change content again
        doc.set_state(content="Hello Alex!")
        print("After edit 3:", doc.title, doc.content)

        # Undo last edit
        caretaker.undo()
        print("After undo:", doc.title, doc.content)

        # Undo last edit
        caretaker.undo()
        print("After undo:", doc.title, doc.content)
        caretaker.display_history_log()

        # Redo last edit
        caretaker.redo()
        print("After redo:", doc.title, doc.content)
        caretaker.display_history_log()

        # Redo last edit
        caretaker.redo()
        print("After redo:", doc.title, doc.content)

        # Save current state to disk
        filepath = caretaker.save_to_disk("document_v1")
        print("Saved memento to:", filepath)
        caretaker.display_history_log()

        # Modify again
        doc.set_state(content="Final Version!")
        print("After final edit:", doc.title, doc.content)

        # Load previous state from disk
        caretaker.load_from_disk(filepath)
        print("After loading from disk:", doc.title, doc.content)
        caretaker.display_history_log()

    def nested_originator_test():
        # Initialize nested Originators
        child1 = Originator(value=10, name="Child1")
        child2 = Originator(value=20, active=True, tags=["a", "b"])

        # Initialize parent Originator with mixed-type attributes
        parent = Originator(
            title="Parent Doc",
            count=5,
            items=[1, 2, 3],
            config={"mode": "test", "enabled": True},
            child1=child1,
            child2=child2
        )

        # Initialize Caretaker
        caretaker = Caretaker(parent)

        print("Initial State:", parent)

        # Modify simple attributes
        parent.set_state(title="Updated Parent Title", count=10)
        print("After parent edit:", parent)

        # Modify nested originator by replacing the object
        parent.set_state(child1=Originator(value=15, name="Child1 Updated"))
        parent.set_state(child2=Originator(value=25, active=False, tags=["x", "y"]))
        print("After nested child updates:", parent)

        # Add new attributes to parent
        parent.set_state(new_attr="Extra", flag=True)
        print("After adding new attributes:", parent)

        # Delete attributes from parent
        parent.delete_state("count", "nonexistent_attr")  # testing deletion of existing and nonexistent
        print("After deleting 'count':", parent)

        # Undo last change
        caretaker.undo()
        print("After undo:", parent)

        # Undo last change
        caretaker.undo()
        print("After undo:", parent)

        # Display history log
        caretaker.display_history_log()

        # Redo last change
        caretaker.redo()
        print("After redo:", parent)

        # Redo last change
        caretaker.redo()
        print("After redo:", parent)

        # Display history log
        caretaker.display_history_log()

        # Save current state
        filepath = caretaker.save_to_disk("nested_doc_test")
        print("Saved memento to:", filepath)

        # Further modify parent and nested attributes
        parent.set_state(title="Final Parent Title", child1=Originator(value=99, name="Child1 Final"))
        print("After final edit:", parent)

        # Load previous state
        caretaker.load_from_disk(filepath)
        print("After loading from disk:", parent)

        # Display history log
        caretaker.display_history_log()

    def nest_test_b():
        # Nested Originators
        child1 = Originator(value=10, name="Child1", active=True)
        child2 = Originator(value=20, active=True, tags=["a", "b"], config={"mode": "dev"})

        # Parent Originator with mixed types
        parent = Originator(
            title="Parent Doc",
            count=5,
            items=[1, 2, 3],
            config={"mode": "test", "enabled": True},
            child1=child1,
            child2=child2
        )

        caretaker = Caretaker(parent)

        print("Initial State:", parent)

        # Modify simple parent attributes
        parent.set_state(title="Updated Parent Title", count=10)
        print("After parent edit:", parent)

        # Multiple child edits
        parent.child1.set_state(value=15, name="Child1 Updated", active=False)
        parent.child2.set_state(value=25, active=False, tags=["x", "y"], config={"mode": "prod"})
        print("After multiple nested child updates:", parent)

        # Add new attributes to parent
        parent.set_state(new_attr="Extra", flag=True)
        print("After adding new attributes:", parent)

        # More child edits
        parent.child1.set_state(name="Child1 Final", notes="important")
        parent.child2.set_state(tags=["final"], config={"mode": "release"}, extra_attr=99)
        print("After additional nested child edits:", parent)
        caretaker.display_history_log()

        # Delete a parent attribute
        parent.delete_state("count")
        print("After deleting 'count':", parent)

        # Undo deletion
        caretaker.undo()
        print("After undo deletion:", parent)

        # Undo last child edit (child2)
        caretaker.undo()
        print("After undo last child2 edit:", parent)

        # Undo previous child edit (child1)
        caretaker.undo()
        print("After undo previous child1 edit:", parent)

        caretaker.display_history_log()

        # Redo child1 edit
        caretaker.redo()
        print("After redo child1 edit:", parent)

        # Redo child2 edit
        caretaker.redo()
        print("After redo child2 edit:", parent)

        # Redo deletion
        caretaker.redo()
        print("After redo deletion:", parent)

        caretaker.display_history_log()

    # simple_originator_test()
    print(f"-------------------------------------------")
    print(f"-------------------------------------------")
    # nested_originator_test()
    nest_test_b()

if __name__ == "__main__":
    main()
