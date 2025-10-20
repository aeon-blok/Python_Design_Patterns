from abc import ABC, abstractmethod
import inspect
import sys

# region Factory Method

# Product (interface)
class Product(ABC):
    """Interface For Concrete Products"""

    def object_info(self):
        """Collects Info about the Current Class and Functions dynamically using Inspect Module"""
        cls = self.__class__
        func_name = inspect.currentframe().f_back.f_code.co_name #type: ignore
        return f"Class Name: {cls.__name__}: This Method is: {func_name}"

    @abstractmethod
    def func_a(self):
        pass

    @abstractmethod
    def func_b(self):
        pass


# Concrete Products
class ConcreteProductA(Product):
    """Concrete Product A Implementation"""

    def func_a(self):  # type: ignore
        return self.object_info()

    def func_b(self):  # type: ignore
        return self.object_info()
    

class ConcreteProductB(Product):
    """Concrete Product B Implementation"""
    def func_a(self):  # type: ignore
        return self.object_info()

    def func_b(self):  # type: ignore
        return self.object_info()


# Creator (interface)
class Creator(ABC):
    """ Interface for Concrete Creators"""
    @abstractmethod
    def factory_method(self) -> Product:
        """Factory Method - Used to choose which Concrete Product to implement inside Concrete Creator Classes."""
        pass

    def func_a(self):
        return self.factory_method().func_a()

    def func_b(self):
        return self.factory_method().func_b()


# Concrete Creators
class ConcreteCreatorA(Creator):
    """Concrete Creator A Implementation"""
    def factory_method(self) -> Product:
        return ConcreteProductA()


class ConcreteCreatorB(Creator):
    """Concrete Creator B Implementation"""
    def factory_method(self) -> Product:
        return ConcreteProductB()

# endregion



# region Client Facing Code
# --- Client Facing Code Usage ---

def dependency_injector(concrete_creator: Creator):
    print(concrete_creator.func_a())
    print(concrete_creator.func_b())


dependency_injector(ConcreteCreatorA())
# endregion
