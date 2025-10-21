from typing import Any, Type, Optional, List
from abc import ABC, ABCMeta, abstractmethod


# Singleton Metaclass
class SingletonMeta(type):
    """
    Ensures only 1 instance per class.
    Important to note: each class that implements the Singleton Metaclass can have 1 instance only of that specific class.
    """

    _singleton = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        """Overrides Class Creation to only Allow 1 instance to be created, if it already exists, just return the existing instance."""
        # existence check - create instance, if it doesnt exist and store in a dictionary.
        if cls not in cls._singleton:
            obj = super().__call__(*args, **kwds)
            cls._singleton[cls] = obj
        return cls._singleton[cls]  # return instance  from dictionary.


# Concrete Class
class Target(metaclass=SingletonMeta):
    def __init__(self, attr_a, attr_b) -> None:  # type: ignore
        self._attr_a = attr_a
        self._attr_b = attr_b

    @property
    def attr_a(self):
        return self._attr_a

    @property
    def attr_b(self):
        return self._attr_b

    def __str__(self):
        return (
            f"Class: {self.__class__.__qualname__} at Memory Address: {hex(id(self))}"
        )


# Main


def main():
    test_class_a = Target(25, 35)
    # instance attributes cannot be initialized again. The original instance and attributes will be returned
    test_class_b = Target("roman", "law")

    print(f"Checking Instance is Singleton:\nInstance A:{test_class_a}\nInstance B: {test_class_b}")
    print(f"Checking Instance Attributes:\nInstance A: {test_class_a.attr_a}, {test_class_a.attr_b}\nInstance B: {test_class_b.attr_a}, {test_class_b.attr_b}")


if __name__ == "__main__":
    main()
