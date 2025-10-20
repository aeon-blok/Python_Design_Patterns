from abc import ABC, abstractmethod
from typing import List, Type
from typing import TYPE_CHECKING
import inspect
import sys


# Abstract Factory (Interface)

class AbstractFactory(ABC):
    """Creates an Interface for Concrete Factories"""

    @abstractmethod
    def create_component_a(self) -> "AbstractProductA":
        """Creates a Specific Class Instance"""
        pass

    @abstractmethod
    def create_component_b(self) -> "AbstractProductB":
        """Creates a Specifc Class Instance"""
        pass

    @abstractmethod
    def create_component_c(self) -> "AbstractProductC":
        """Creates a Specific Class Instance"""
        pass


# Concrete Factories
class FactoryA(AbstractFactory):
    """Factory Just Creates Specific Class Instances"""
    def create_component_a(self):
        return ProductA1()

    def create_component_b(self):
        return ProductA2()

    def create_component_c(self):
        return ProductA3()


class FactoryB(AbstractFactory):
    """Factory Just Creates Specific Class Instances"""

    def create_component_a(self):
        return ProductB1()

    def create_component_b(self):
        return ProductB2()

    def create_component_c(self):
        return ProductB3()


# Abstract Products (Interface)
class AbstractProductA(ABC):
    """Interface for a Specific Concrete Product"""
    @abstractmethod
    def func_a(self) -> str:
        """Performs some Functionality"""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Info About the Class"""
        pass


class AbstractProductB(ABC):
    """Interface for a Specific Concrete Product"""

    @abstractmethod
    def func_a(self) -> str:
        """Performs some Functionality"""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Info About the Class"""
        pass


class AbstractProductC(ABC):
    """Interface for a Specific Concrete Product"""

    @abstractmethod
    def func_a(self) -> str:
        """Performs some Functionality"""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Info About the Class"""
        pass


# Products



# Factory A Products
class ProductA1(AbstractProductA):
    def func_a(self):
        func_name = inspect.currentframe().f_code.co_name  # type: ignore
        return f"Class: {self.__class__.__name__} Executes Function: {func_name}"

    def __str__(self) -> str:
        return f"Class: {self.__class__.__name__}"


class ProductA2(AbstractProductB):

    def func_a(self):
        func_name = inspect.currentframe().f_code.co_name  # type: ignore
        return f"Class: {self.__class__.__name__} Executes Function: {func_name}"

    def __str__(self) -> str:
        return f"Class: {self.__class__.__name__}"


class ProductA3(AbstractProductC):

    def func_a(self):
        func_name = inspect.currentframe().f_code.co_name  # type: ignore
        return f"Class: {self.__class__.__name__} Executes Function: {func_name}"

    def __str__(self) -> str:
        return f"Class: {self.__class__.__name__}"


# Factory B Products
class ProductB1(AbstractProductA):

    def func_a(self):
        func_name = inspect.currentframe().f_code.co_name  # type: ignore
        return f"Class: {self.__class__.__name__} Executes Function: {func_name}"

    def __str__(self) -> str:
        return f"Class: {self.__class__.__name__}"


class ProductB2(AbstractProductB):

    def func_a(self):
        func_name = inspect.currentframe().f_code.co_name  # type: ignore
        return f"Class: {self.__class__.__name__} Executes Function: {func_name}"

    def __str__(self) -> str:
        return f"Class: {self.__class__.__name__}"


class ProductB3(AbstractProductC):

    def func_a(self):
        func_name = inspect.currentframe().f_code.co_name  # type: ignore
        return f"Class: {self.__class__.__name__} Executes Function: {func_name}"

    def __str__(self) -> str:
        return f"Class: {self.__class__.__name__}"


# Main

def main():

    # Dependency Injector for Factory
    def abstract_factory(factory_cls: Type[AbstractFactory]):
        """Loads the User Defined Abstract factory"""
        factory = factory_cls() # instantiates the class
        product_1 = factory.create_component_a()
        product_2 = factory.create_component_b()
        product_3 = factory.create_component_c()

        # inline assertations for dev
        assert isinstance(product_1, AbstractProductA)
        assert isinstance(product_2, AbstractProductB)
        assert isinstance(product_3, AbstractProductC)

        # generic information to show the pattern works.
        print(product_1)
        print(product_2)
        print(product_3)

        # Trying the factory component functions
        print(product_1.func_a())
        print(product_2.func_a())
        print(product_3.func_a())


    # Client Facing Code - implementing the DI Injector
    abstract_factory(FactoryA)
    abstract_factory(FactoryB)


if __name__ == "__main__":
    main()
