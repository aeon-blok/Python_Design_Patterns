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


# target (new interface) -- client needs this. This is the interface the client will use
class Target:
    """Client inteface they wish to use"""
    
    def request(self):
        raise NotImplementedError


# adapter (translates old interface to new interface)
class Adapter(Target):
    """Translates between the Client / Target (new interface) and the Adaptee (old interface)"""

    def __init__(self, adaptee: "Adaptee",**kwargs) -> None:
        self._adaptee = copy.deepcopy(adaptee)  # composed adaptee object deep copy.
        self._adapter_data = kwargs

    def _transform_data(self, adaptee_output: dict):
        """Transforms data from Adaptee via Adapter. Attributes from both will be kept and presented. Adapter attributes will overwrite Adaptee."""
        adapter_output = {}

        # overwrites keys from adaptee
        for key, value in adaptee_output.items():
            new_key = f"Adapter {key}"
            adapter_output[new_key] = self._adapter_data.get(key, value)

        # adds keys not in adaptee
        for key, value in self._adapter_data.items():
            new_key = f"Adapter {key}"
            if new_key not in adapter_output:
                adapter_output[new_key] = value

        return adapter_output

    def _format_data(self, adaptee_output, adapter_output):
        """ Formats transformed Adaptee Data into a readable string for human readability"""
        adaptee_string = f"\n".join(f"{k} = {v}" for k, v in adaptee_output.items())
        adapter_string = f"\n".join(f"{k} = {v}" for k, v in adapter_output.items())
        return (f"Adaptee:\n{adaptee_string}\n\nConverts To:\n\nAdapter:\n{adapter_string}")

    def request(self):
        """Transforms Adaptee functionality into something that can be used by the new interface"""
        adaptee_output = self._adaptee.specific_request()
        adapter_output = self._transform_data(adaptee_output)
        return self._format_data(adaptee_output, adapter_output)


# adaptee (old interface) -- client has this (existing interface to legacy functionality)
class Adaptee:
    """Old Interface & Functionality from Legacy program"""
    def __init__(self, **kwargs) -> None:
        self._adaptee_data = kwargs

    def specific_request(self):
        """Legacy Functionality that is required in new program"""
        return self._adaptee_data


# client
class Client:
    """Client Facing API - executes the desired functionality (which gets translated by Adapter)"""
    def __init__(self, adapter: Target) -> None:
        self._adapter = adapter

    def request(self):
        """runs Adapter method (Which transforms Adaptee method)"""
        return self._adapter.request()


# Main - Client Facing Code
def main():
    old_interface = Adaptee(speed=25, timeframe="ancient")
    new_interface = Adapter(old_interface, speed=100, era="modern")
    print(Client(new_interface).request())


if __name__ == "__main__":
    main()
