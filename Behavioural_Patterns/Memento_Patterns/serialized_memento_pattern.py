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

# pyright: reportGeneralTypeIssues=false

# Memento
class iMemento(ABC):

    @abstractmethod
    def get_snapshot(self) -> "iOriginator":
        pass


class Memento(iMemento):
    """receives a deep copy of an objects internal state. which it can provide on request"""
    def __init__(self, state) -> None:
        self._state = copy.deepcopy(state)

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


class Originator(iOriginator):
    """ Target Object that shares its internal state to the Memento. extra functionality for whatever the object is needed for..."""
    
    def __getattr__ (self, name) -> any:
        """Override getattr to remove type hint errors (dynamic attributes)"""
        return self.__dict__.get(name, Any)
    
    
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_state(self, **kwargs):
        """Helper Method - that redefines attributes for the class dynamically."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_state(self):
        """ returns the object instance"""
        return self

    def create_memento(self) -> iMemento:
        """Creates a Snapshot of the internal state of the object (its the whole object), that it sends to the Memento"""
        return Memento(self)

    def restore_memento(self, memento: iMemento) -> None:
        """restores a previously saved snapshot of the internal state, and updates the current internal state to match."""
        snapshot = memento.get_snapshot()
        self.__dict__.clear()
        self.__dict__.update(snapshot.__dict__)


# Caretaker
class iCaretaker(ABC):

    @abstractmethod
    def record(self) -> iMemento:
        pass

    @abstractmethod
    def undo(self) -> None | str:
        pass

    @abstractmethod
    def redo(self) -> None | str:
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
        self._undo_stack: list[iMemento] = []
        self._undo_stack.append(originator.create_memento())    # initialize first undo save point
        self._redo_stack: list[iMemento] = []
        self._directory = Path(directory)
        self._directory.mkdir(exist_ok=True)
        self._originator = originator

    def record(self) -> iMemento:
        """creates a restore checkpoint for undo / redo functionality."""
        memento = self._originator.create_memento()
        self._undo_stack.append(memento)
        self._redo_stack.clear()
        return memento

    def undo(self) -> None | str:
        """Undo Functionality - returns back to the last record checkpoint"""
        if len(self._undo_stack) < 2:
            return f"undo: nothing to undo..."

        current = self._undo_stack.pop()
        self._redo_stack.append(current)

        previous = self._undo_stack[-1]
        self._originator.restore_memento(previous)

    def redo(self) -> None | str:
        """redo functionality - returns back to last undo."""
        if not self._redo_stack:
            return f"redo: nothing to redo..."
        memento = self._redo_stack.pop()
        self._undo_stack.append(memento)
        self._originator.restore_memento(memento)

    def save_to_disk(self, filename) -> Path:
        """Saves a Memento to disk as a pickle file."""
        memento = self._undo_stack[-1]
        filename = f"{filename}.pickle"
        filepath = self._directory / filename
        with open(filepath, "wb") as file:
            pickle.dump(memento, file)
        return filepath

    def load_from_disk(self, filepath) -> None:
        """Loads a Memento pickle file from disk"""

        if not filepath.is_file():
            raise ValueError (f"{filepath}: does not exist!")

        with open(filepath, "rb") as file:
            memento = pickle.load(file)

        self._undo_stack.append(memento)
        self._originator.restore_memento(memento)
        self._redo_stack.clear()


# Main
def main():
    # Initialize
    environment = Originator(
        name="The Desert of kalcakacl", biome="arctic desert", weather="Windy"
    )
    inventory = Originator(scroll="Scroll of Doom", arrows="Fire Arrows", gold=250)

    character = Originator(
        name="The Dwarf",
        hp=100,
        damage=25,
        armour="Steel Breastplate",
        inventory=inventory,
    )
    game = Originator(character=character, environment=environment)

    manager = Caretaker(game)

    print(game.character.name) 

    # --- Initial State ---
    print("=== Initial State ===")
    print(
        "Character:",
        game.character.name,
        "HP:",
        game.character.hp,
        "Damage:",
        game.character.damage,
    )
    print("Inventory:", game.character.inventory.scroll, game.character.inventory.gold)
    print(
        "Environment:",
        game.environment.name,
        game.environment.biome,
        game.environment.weather,
    )

    # Record first checkpoint
    manager.record()

    # Modify nested objects
    game.character.hp = 75
    game.character.damage = 30
    game.character.inventory.gold = 300

    print("\n=== After Damage + Inventory Change ===")
    print(
        "Character:",
        game.character.name,
        "HP:",
        game.character.hp,
        "Damage:",
        game.character.damage,
    )
    print("Inventory:", game.character.inventory.scroll, game.character.inventory.gold)

    # Record second checkpoint
    manager.record()

    # Undo
    manager.undo()
    print("\n=== After Undo ===")
    print(
        "Character:",
        game.character.name,
        "HP:",
        game.character.hp,
        "Damage:",
        game.character.damage,
    )
    print("Inventory:", game.character.inventory.scroll, game.character.inventory.gold)

    # Redo
    manager.redo()
    print("\n=== After Redo ===")
    print(
        "Character:",
        game.character.name,
        "HP:",
        game.character.hp,
        "Damage:",
        game.character.damage,
    )
    print("Inventory:", game.character.inventory.scroll, game.character.inventory.gold)

    # Save to disk
    save_file = manager.save_to_disk("game_save")
    print(f"\nSaved current state to disk: {save_file}")

    # Further changes
    game.character.hp = 50
    game.character.inventory.scroll = "Scroll of Lightning"
    print("\n=== After Further Changes ===")
    print(
        "Character:",
        game.character.name,
        "HP:",
        game.character.hp,
        "Damage:",
        game.character.damage,
    )
    print("Inventory:", game.character.inventory.scroll, game.character.inventory.gold)

    # Load from disk (undo all changes)
    manager.load_from_disk(save_file)
    print(f"\nLoaded from disk: {save_file}")
    print(
        "Character:",
        game.character.name,
        "HP:",
        game.character.hp,
        "Damage:",
        game.character.damage,
    )
    print("Inventory:", game.character.inventory.scroll, game.character.inventory.gold)

if __name__ == "__main__":
    main()
