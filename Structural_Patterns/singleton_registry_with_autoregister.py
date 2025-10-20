from typing import Type
from abc import ABC, ABCMeta, abstractmethod


# Singleton Registry - Class Based Singleton
class Registry:
    """Registry Container for Classes. (Class Based Singleton)"""
    _data: dict[str, Type["Product"]] = {}

    @classmethod
    def register(cls, label: str, concrete_cls: Type["Product"]):
        """Registers a Class with the Registry."""
        if label in cls._data:
            raise KeyError(f"'{label}' is already registered")
        cls._data[label] = concrete_cls

    @classmethod
    def create(cls, label: str, *args, **kwargs) -> "Product":
        """Instantiates a Class from the registry. Args and Kwargs can be passed to the Class __init__ Constructor"""
        concrete_cls = cls._data.get(label)
        if concrete_cls is None:
            raise ValueError(f"Class: {label}: Not Found in Registry. Available: {list(cls._data.keys())}")
        return concrete_cls(*args, **kwargs)

    @classmethod
    def display_items(cls):
        """Displays all the classes currently contained in the Registry"""
        for label, cls in cls._data.items():
            print(f"Registry Item: {label} at Memory Address: {hex(id(cls))}")


# Metaclass
class AutoRegister(ABCMeta):
    """Metaclass that automatically adds classes to a Registry (class based singleton)"""
    def __init__(cls, name, bases, namespace):
        # Only register concrete subclasses (no abstract methods left)
        if not getattr(cls, "__abstractmethods__", None):
            # calls class method straight from Registry() class.
            Registry.register(name, cls)  # type: ignore
        super().__init__(name, bases, namespace)


# Product (Interface) -- Metaclass means that any subclasses of Product will be automatically registered.
class Product(ABC, metaclass=AutoRegister):
    """Interface for Auto Registered Classes"""
    @abstractmethod
    def func_a(self):
        pass


# Concrete Products
class ClassA(Product):
    """Class Implementation"""
    def func_a(self):
        print(self.__class__.__qualname__)


class ClassB(Product):
    """Class Implementation"""
    def func_a(self):
        print(self.__class__.__qualname__)


class ClassC(Product):    
    """Class Implementation"""
    def func_a(self):
        print(self.__class__.__qualname__)


# --- Client Facing Code Usage ---


def main():

    # list all Classes in the registry
    Registry.display_items()

    # Instantiate Classes
    class_A = Registry.create("ClassA")
    class_A.func_a()
    # Can call functions on the same line as instantiation
    class_B = Registry.create("ClassB").func_a()


if __name__ == "__main__":
    main()
