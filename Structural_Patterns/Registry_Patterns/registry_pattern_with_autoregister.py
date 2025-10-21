from abc import ABC, ABCMeta, abstractmethod
from typing import Type

# Global Registry (dictionary) -- Stores Classes not Objects.
REGISTRY: dict[str, Type['Product']] = {}

# Metaclass that auto-registers classes of a specific type.
class AutoRegister(ABCMeta):    # has to inherit from ABC Meta for subclasses conflict issue
    def __init__(cls, name, bases, namespace):

        if name in REGISTRY:  # existence check
            raise KeyError(f"'{name}' is already registered")

        # No abstract methods in this class - register it.
        if not getattr(cls, "__abstractmethods__", False):
            REGISTRY[name] = cls    # type: ignore

        # Call original class __init__
        super().__init__(name, bases, namespace)


# Product (Interface)
class Product(ABC, metaclass=AutoRegister):
    @abstractmethod
    def func_a(self):
        pass

# Concrete Products (These will be automatically added to the registry.)

class ClassA(Product):
    def func_a(self):
        return print(self.__class__.__qualname__)


class ClassB(Product):
    def func_a(self):
        return print(self.__class__.__qualname__)


class ClassC(Product):
    def func_a(self):
        return print(self.__class__.__qualname__)


# --- Client Code Usage ---

def main():

    # iterating through all the auto registered classes in the dictionary.
    for label, item in REGISTRY.items():
        print(f"Registered class: {label} -> {hex(id(item))}")

    # Access by Name & Create Instance:
    class_A = REGISTRY['ClassA']()  # instantiate with the ()

    # Call Method
    class_A.func_a()


if __name__ == "__main__":
    main()
