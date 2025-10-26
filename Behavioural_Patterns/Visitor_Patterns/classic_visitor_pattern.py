from threading import Lock
from enum import Enum
from dataclasses import dataclass, field
import copy
import inspect
from collections.abc import Iterable
from typing import Any, Type, Optional, List, Dict
from abc import ABC, ABCMeta, abstractmethod
import pickle
from pathlib import Path
from datetime import datetime
from pprint import pprint

# Visitor (interface)
class iVisitor(ABC):
    """Visitor interface with visit_element_X() methods for each element type"""

    @abstractmethod
    def visit_element_a(self, element: "iElement"):
        """Visit Method: a method defined in a Visitor that performs an operation on an element."""
        pass

    @abstractmethod
    def visit_element_b(self, element: "iElement"):
        """Visit Method: a method defined in a Visitor that performs an operation on an element."""
        pass

    @abstractmethod
    def visit_element_c(self, element: "iElement"):
        """Visit Method: a method defined in a Visitor that performs an operation on an element."""
        pass


# Concrete Visitor (Hold Behaviour)
class Visitor(iVisitor):
    """Defines the Behaviour that will run for each element. Context is derived from the element itself"""
    def __init__(self, **kwargs) -> None:
        self._state: dict[str, Any] = kwargs
        self._matches: Dict[str, Dict[str, Dict[str, Any]]] = {}


    # Functionality: (Find Matching Keys)
    def _find_matching_keys(self, element: "iElement"):
        """store the values for visitor and element in matches:"""
        element_name = element.name # type: ignore

        shared_keys = set(self._state.keys()) & set(element._state.keys())   # set intersection

        for key in shared_keys: # loops through shared keys and adds to dict
            element_dict = self._matches.setdefault(element_name, {})   # create key in self._matches dict 
            # add nested dict structure with data.
            element_dict[key] = {
                "visitor_value": self._state[key], 
                "element_value": element._state[key],
                }

    def get_matches_for_element(self, element_name):
        """Returns all keys and their values for that specific element."""
        return self._matches.get(element_name, {})

    def get_all_elements(self):
        """Return a list of all elements that have matches"""
        return list(self._matches.keys())

    def get_all_keys(self):
        """retrieves all matched unique keys across all elements."""
        return {element: set(keys.keys()) for element, keys in self._matches.items()}

    def count_key_matches_for_element(self, element_name):
        """Returns total key matches for a specific element"""
        return len(self._matches.get(element_name, {}))

    def count_total_key_matches(self):
        """Returns total key matches across all elements"""
        return sum(len(keys) for element, keys in self._matches.items())

    def get_all_matches(self):
        """Returns a deep copy of the self._matches dict"""
        return copy.deepcopy(self._matches)

    def reset_match_storage(self):
        """reset the self._matches dictionary"""
        self._matches = {}

    def infostring(self, element: "iElement"):
        """Displays information about the Element and the Key Matches"""
        string_visitor = f"Visiting {element.__class__.__qualname__}: Instance: {element.name}..."
        print(string_visitor)
        infostring = f"Class: {element.__class__.__qualname__}: We found total key matches of: {self.count_key_matches_for_element(element.name)} for:  Name: {element.name}"
        print(infostring)
        elements_match = self.get_matches_for_element(element.name)
        print(f"Displaying Matches....")
        pprint(elements_match)


    # visit methods
    def visit_element_a(self, element: "iElement"):
        self._find_matching_keys(element)
        self.infostring(element)

    def visit_element_b(self, element: "iElement"):
        self._find_matching_keys(element)
        self.infostring(element)

    def visit_element_c(self, element: "iElement"):
        self._find_matching_keys(element)
        self.infostring(element)


# Element (Interface)
class iElement(ABC):
    """Element Interface: - mandatory accept_visitor()"""
    @abstractmethod
    def accept_visitor(self, visitor: iVisitor):
        pass


# Concrete Elements (Targets) (Hold Data)
class ElementA(iElement):
    """Stores Data that the Visitor will utilize with its own behaviour"""
    def __init__(self, name: str, **kwargs) -> None:
        self._name = name
        self._state = kwargs

    @property
    def name(self):
        return self._name

    def accept_visitor(self, visitor: iVisitor):
        """Coupled to a specific visitor. Used to execute Visitor Visit Method..."""
        visitor.visit_element_a(self)   # element injection - itself...


class ElementB(iElement):
    """Stores Data that the Visitor will utilize with its own behaviour"""

    def __init__(self, name: str, **kwargs) -> None:
        self._name = name
        self._state = kwargs

    @property
    def name(self):
        return self._name

    def accept_visitor(self, visitor: iVisitor):
        """Coupled to a specific visitor. Used to execute Visitor Visit Method..."""
        visitor.visit_element_b(self)


class ElementC(iElement):
    """Stores Data that the Visitor will utilize with its own behaviour"""

    def __init__(self, name: str, **kwargs) -> None:
        self._name = name
        self._state = kwargs

    @property
    def name(self):
        return self._name

    def accept_visitor(self, visitor: iVisitor):
        """Coupled to a specific visitor. Used to execute Visitor Visit Method..."""
        visitor.visit_element_c(self)


# Main -- Client Facing Code
def main():
    # initialize elements
    element_a = ElementA(name="Document A", size=2500, wordcount=250654, working_title="The Ages of Despair...", author="Unknown")
    element_b = ElementB(name="Document B", emotional_impact="vivid", working_title="The Claws of Tooth Decay...", author="Bronte Dansaour")
    element_c = ElementC(name="Document C", knowledge_base ="ISO: 054357", working_title="I thought i saw a sign...", author="Grent Cunningwoods")
    
    element_list = [element_a, element_b, element_c] # add to a list

    # initialize Visitor
    visitor = Visitor(working_title=None)

    # Call Visitor for each element...
    for items in element_list:
        items.accept_visitor(visitor)

    # ! Utilize visitor behaviour
    print(f"\nGet all matches from Visitor (finds keys with the same key name. )")
    pprint(visitor.get_all_matches())

    print(f"\nGet all matching keys (only) from Visitor")
    pprint(visitor.get_all_keys())

    print(f"\nGet all Element Names (only) that have matches from Visitor")
    pprint(visitor.get_all_elements())


if __name__ == "__main__":
    main()
