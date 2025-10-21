from typing import Any, Type, Optional, List
from abc import ABC, ABCMeta, abstractmethod
from threading import Lock


# Strategy (Interface)


class Strategy(ABC):
    """Interface for strategies"""

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def func_a(self, attr_a: int, attr_b: int) -> int:
        pass


# Concrete Strategies


class ConcreteStrategyA(Strategy):
    """Specific Strategy Implementation - defines what the algorithm does"""

    def __init__(self, attr_c: int) -> None:
        self._attr_c = attr_c

    def __str__(self) -> str:
        return (
            f"Class: {self.__class__.__qualname__} at Memory Address: {hex(id(self))}"
        )

    def func_a(self, attr_a, attr_b) -> int:
        result = self._attr_c * attr_a * attr_b
        return result


class ConcreteStrategyB(Strategy):
    """Specific Strategy Implementation - defines what the algorithm does"""

    def __init__(self, attr_c: int, attr_d: int) -> None:
        self._attr_c = attr_c
        self._attr_d = attr_d

    def __str__(self) -> str:
        return (
            f"Class: {self.__class__.__qualname__} at Memory Address: {hex(id(self))}"
        )

    def func_a(self, attr_a, attr_b) -> int:
        result = self._attr_c * attr_a * attr_b * self._attr_d
        return result


class ConcreteStrategyC(Strategy):
    """Specific Strategy Implementation - defines what the algorithm does"""

    def __init__(self, attr_c: int, attr_d: int, attr_e: int) -> None:
        self._attr_c = attr_c
        self._attr_d = attr_d
        self._attr_e = attr_e

    def __str__(self) -> str:
        return (
            f"Class: {self.__class__.__qualname__} at Memory Address: {hex(id(self))}"
        )

    def func_a(self, attr_a, attr_b) -> int:
        result = self._attr_c * attr_a * attr_b * self._attr_d * self._attr_e
        return result


# Context (Selector)


class Context:
    """
    Context defines when and HOW a strategy is used...
    Context is responsible for the workflow that wraps around the algorithm.
    """

    def __init__(self, strategy: Strategy):
        self._strategy = strategy
        pass

    def set_strategy(self, strategy: Strategy):
        """Can dynamically change strategy at runtime"""
        self._strategy = strategy

    def perform_func_a(self, attr_a: int, attr_b: int):
        """Performs Functionality -- requires input from both the Context & the Concrete Strategy"""
        return self._strategy.func_a(attr_a, attr_b)


# Main --- Client Facing Code ---


def main():

    # initialize strategies
    strategy_a = ConcreteStrategyA(2)
    strategy_b = ConcreteStrategyB(2, 3)
    strategy_c = ConcreteStrategyC(4, 5, 6)

    # choose strategy and add context data
    context = Context(strategy_b)
    result = context.perform_func_a(2, 2)
    print(result)

if __name__ == "__main__":
    main()
