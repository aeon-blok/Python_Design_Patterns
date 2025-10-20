from abc import ABC, abstractmethod
import inspect
import sys


# Product (Interface)
class Product(ABC):

    def object_info(self):
        """Collects Info about the Current Class and Functions dynamically using Inspect Module"""
        cls = self.__class__
        func_name = inspect.currentframe().f_back.f_code.co_name  # type: ignore
        return f" This Method is: {func_name} From Class: {cls.__name__}:"

    @abstractmethod
    def func_a(self):
        pass

    @abstractmethod
    def func_b(self):
        pass


# Concrete Product
class ConcreteProductA(Product):
    """Concrete Product Implementation of the Product Interface"""
    def func_a(self): # type: ignore
        return self.object_info()

    def func_b(self):  # type: ignore
        return self.object_info()


class ConcreteProductB(Product):
    """Concrete Product Implementation of the Product Interface"""
    def func_a(self):  # type: ignore
        return self.object_info()

    def func_b(self):  # type: ignore
        return self.object_info()


class ConcreteProductC(Product):
    """Concrete Product Implementation of the Product Interface"""
    def func_a(self):  # type: ignore
        return self.object_info()

    def func_b(self):  # type: ignore
        return self.object_info()


# Factory
class Factory:
    """Simple Factory Class - Creates an Instance of a Concrete Product. You can choose which one."""
    @staticmethod
    def create_product(concrete_product_type: type[Product]) -> Product:
        # this code allows us to extend,add & use Concrete Products without having to modify this class.
        if not issubclass(concrete_product_type, Product):
            raise ValueError("ERROR: Unknown Concrete Product Type!")
        return concrete_product_type()  # instantiates the Concrete Product Class.


# --- Client Facing Code ---

# initializing the factory
new_factory = Factory()

# creating Concrete Product Instances
concrete_product_a = new_factory.create_product(ConcreteProductA)
concrete_product_b = new_factory.create_product(ConcreteProductB)
concrete_product_c = new_factory.create_product(ConcreteProductC)

# Testing the Methods for each Instance
print(concrete_product_a.func_a())
print(concrete_product_a.func_b())

print(concrete_product_b.func_a())
print(concrete_product_b.func_b())

print(concrete_product_c.func_a())
print(concrete_product_c.func_b())
