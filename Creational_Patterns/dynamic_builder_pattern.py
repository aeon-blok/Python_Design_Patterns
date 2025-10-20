from abc import ABC, abstractmethod
from typing import List, Type
from typing import TYPE_CHECKING
import inspect
import sys


# region Components


# Component Interface
class CompInterface(ABC):
    """Interface for individual components"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Each component must expose a name"""
        pass

    @abstractmethod
    def info(self) -> str:
        """Component Info String - Contains Name and Attributes (Parsed via *Args & **Kwargs)"""
        pass


# Concrete Components
class Component(CompInterface):
    """Component Object"""

    def __init__(self, name: str, *args, **kwargs) -> None:
        self._name = name
        self._args = args
        self._kwargs = kwargs

        # Automatically add kwargs as attributes
        for key, value in self._kwargs.items():
            setattr(self, key, value)

        # map positional args to indexed attributes (arg0, arg1, ...)
        for i, value in enumerate(self._args):
            setattr(self, f"arg{i}", value)

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def name(self):
        return self._name

    def info(self):
        """Displays the Component's Name and Attributes"""
        parsed_args = ", ".join(repr(arg) for arg in self._args)
        parsed_kwargs = ", ".join(
            f"{key}={value}" for key, value in self._kwargs.items()
        )
        component_attributes = ", ".join(filter(None, [parsed_args, parsed_kwargs]))
        return f"Component Name: {self._name}: Attributes: {component_attributes}"


# endregion


# region Product


# Product (Interface)
class Product(ABC):
    """Interface for the final product"""

    @abstractmethod
    def freeze(self):
        pass

    @abstractmethod
    def set_component(self, component: "CompInterface"):
        pass

    @abstractmethod
    def get_component(self, component: "CompInterface") -> CompInterface:
        pass

    @abstractmethod
    def display_components(self):
        pass


# Concrete Product -- this is the final complex object that gets seperated into pieces.
class ConcreteProductA(Product):
    """Concrete Implementation of the final object."""

    def __init__(self):
        self._components: dict[str, CompInterface] = {}  # stores components
        self._frozen: bool = False

    def freeze(self):
        """Ensures that the Concrete Product cannot be modified after it has been built"""
        self._frozen = True

    def set_component(self, component: "CompInterface"):
        """Used to store Component Class Instances in the Concrete Product"""
        if self._frozen:
            raise RuntimeError(f"Product is Frozen. Can no longer modify this Product!")
        if not isinstance(component, CompInterface):
            raise TypeError(
                f"Expected A Component Object, got {type(component).__name__}"
            )
        self._components[component.name] = component

    def get_component(self, component: "CompInterface"):
        """Retrieves a single Component Class Instance from the product"""
        print(f"Retrieving Component: {component.name}")
        return self._components[component.name]

    def display_components(self):
        """Displays all the components in the Concrete Product"""
        print(f"Class: {self.__class__.__qualname__} owns the Following Components: ")
        for component in self._components.values():
            print(component.info())


# endregion


# region Builder


# Builder (Interface)
class iBuilder(ABC):
    """Interface for Concrete Builder"""

    def __init__(self, concrete_product: Type[Product]):
        self._concrete_product = concrete_product()

    @abstractmethod
    def add(self, *components: "CompInterface") -> "iBuilder":
        pass

    def build(self) -> Product:
        self._concrete_product.freeze()
        return self._concrete_product


# Concrete Builder
class DynamicBuilder(iBuilder):
    """Assembles the Final Product in a Unique Representation (ordering can change.)"""

    def add(self, *components: CompInterface) -> "DynamicBuilder":
        """Adds Components to the Product. Can add more than 1 per add method. Also can chain methods via fluent interface"""
        for item in components:
            self._concrete_product.set_component(item)
        return self


# endregion


# region Main


# --- Client Facing Code Usage ---
def main():

    # Manual Build
    # components
    engine = Component("Engine", "V8", turbo=True)
    wheel1 = Component("Wheel Front Left", 20, wheel_type="Offroad")
    wheel2 = Component("Wheel Front Right", 20, wheel_type="Offroad")
    color = Component("Body Color", "Red", finish="Metallic")

    # builder
    product = (
        DynamicBuilder(ConcreteProductA)
        .add(engine)
        .add(wheel1, wheel2)
        .add(color)
        .build()
    )

    # display product information (all components and their attributes.)
    product.display_components()

    # retrieve individual component
    color_component = product.get_component(color)
    engine_component = product.get_component(engine)

    # accessing attributes of Component
    print(engine_component.turbo)   # type: ignore   # **kwargs attribute
    print(engine_component.arg0)    # type: ignore   # *args attribute


if __name__ == "__main__":
    main()

# endregion
