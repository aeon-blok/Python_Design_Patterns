from abc import ABC, abstractmethod
from typing import List, Type
from typing import TYPE_CHECKING
import inspect
import sys


# region Product


# Product (Interface)
class Product(ABC):
    """Interface for the final product"""

    @abstractmethod
    def get_component(self, component_cls: type["CompInterface"]) -> "CompInterface":
        pass

    @abstractmethod
    def freeze(self) -> None:
        """Prevents any further modification to the Components. usually implemented in the build() method."""
        pass

    @abstractmethod
    def set_component_a(self, component: "CompInterface"):
        pass

    @abstractmethod
    def set_component_b(self, component: "CompInterface"):
        pass

    @abstractmethod
    def set_component_c(self, component: "CompInterface"):
        pass

    @abstractmethod
    def set_component_d(self, component: "CompInterface"):
        pass

    @abstractmethod
    def list_components(self):
        pass


# Concrete Product A -- this is the final complex object that gets seperated into pieces.
class ConcreteProductA(Product):
    """Concrete Implementation of the final object."""

    def __init__(self) -> None:
        self._ComponentA: CompInterface | None = None
        self._ComponentB: CompInterface | None = None
        self._ComponentC: CompInterface | None = None
        self._ComponentD: CompInterface | None = None
        self._frozen: bool = False

    def freeze(self) -> None:
        self._frozen = True

    def _freeze_error(self):
        raise RuntimeError(f"Class: {self.__class__.__qualname__} is currently Frozen. Cannot Modify the components.")

    def set_component_a(self, component: "CompInterface"):
        self._ComponentA = component if not self._frozen else self._freeze_error()

    def set_component_b(self, component: "CompInterface"):
        self._ComponentB = component if not self._frozen else self._freeze_error()

    def set_component_c(self, component: "CompInterface"):
        self._ComponentC = component if not self._frozen else self._freeze_error()

    def set_component_d(self, component: "CompInterface"):
        self._ComponentD = component if not self._frozen else self._freeze_error()

    def get_component(self, component_cls: type["CompInterface"]) -> "CompInterface":
        for value in vars(self).values():
            if isinstance(value, component_cls):
                return value
        # Gets the component names only via type
        components_only = [type(comp).__name__ for comp in vars(self).values() if isinstance(comp, CompInterface)]
        raise ValueError(
            f"Component: {component_cls.__name__} is not Valid! Available components are: {components_only}"
        )

    def list_components(self):
        print(f"Class: {self.__class__.__qualname__}")
        # filters all attributes of the class (vars(self)) by Type
        for value in filter(
            lambda value: isinstance(value, CompInterface), vars(self).values()
        ):
            print(value.__repr__())


# Concrete Product B
class ConcreteProductB(Product):
    """Concrete Implementation of the final object."""

    def __init__(self) -> None:
        self._ComponentA: CompInterface | None = None
        self._ComponentB: CompInterface | None = None
        self._ComponentC: CompInterface | None = None
        self._ComponentD: CompInterface | None = None
        self._frozen: bool = False

    def freeze(self) -> None:
        self._frozen = True

    def _freeze_error(self):
        raise RuntimeError(
            f"Class: {self.__class__.__qualname__} is currently Frozen. Cannot Modify the components."
        )

    def set_component_a(self, component: "CompInterface"):
        self._ComponentA = component if not self._frozen else self._freeze_error()

    def set_component_b(self, component: "CompInterface"):
        self._ComponentB = component if not self._frozen else self._freeze_error()

    def set_component_c(self, component: "CompInterface"):
        self._ComponentC = component if not self._frozen else self._freeze_error()

    def set_component_d(self, component: "CompInterface"):
        self._ComponentD = component if not self._frozen else self._freeze_error()

    def get_component(self, component_cls: type["CompInterface"]) -> "CompInterface":
        for value in vars(self).values():
            if isinstance(value, component_cls):
                return value
        # Gets the component names only via type
        components_only = [
            type(comp).__name__
            for comp in vars(self).values()
            if isinstance(comp, CompInterface)
        ]
        raise ValueError(
            f"Component: {component_cls.__name__} is not Valid! Available components are: {components_only}"
        )

    def list_components(self):
        print(f"Class: {self.__class__.__qualname__}")
        # filters all attributes of the class (vars(self)) by Type
        for value in filter(
            lambda value: isinstance(value, CompInterface), vars(self).values()
        ):
            print(value.__repr__())


# endregion


# region Components


# Component Interface
class CompInterface(ABC):
    """Interface for individual components"""

    @abstractmethod
    def __init__(self, name: str, attr_a: str, attr_b: str) -> None:
        """All components must have these parameters"""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


# Concrete Components
class ComponentA(CompInterface):
    """Component Object"""

    def __init__(self, name: str, attr_a: str, attr_b: str) -> None:
        self._name = name
        self._attr_a = attr_a
        self._attr_b = attr_b

    def __repr__(self):
        return f"Component Class: [{self.__class__.__qualname__}] Category: [{self._name}] Attributes: [{self._attr_a}][{self._attr_b}]"


class ComponentB(CompInterface):
    """Component Object"""

    def __init__(self, name: str, attr_a: str, attr_b: str) -> None:
        self._name = name
        self._attr_a = attr_a
        self._attr_b = attr_b

    def __repr__(self):
        return f"Component Class: [{self.__class__.__qualname__}] Category: [{self._name}] Attributes: [{self._attr_a}][{self._attr_b}]"


class ComponentC(CompInterface):
    """Component Object"""

    def __init__(self, name: str, attr_a: str, attr_b: str) -> None:
        self._name = name
        self._attr_a = attr_a
        self._attr_b = attr_b

    def __repr__(self):
        return f"Component Class: [{self.__class__.__qualname__}] Category: [{self._name}] Attributes: [{self._attr_a}][{self._attr_b}]"


class ComponentD(CompInterface):
    """Component Object"""

    def __init__(self, name: str, attr_a: str, attr_b: str) -> None:
        self._name = name
        self._attr_a = attr_a
        self._attr_b = attr_b

    def __repr__(self):
        return f"Component Class: [{self.__class__.__qualname__}] Category: [{self._name}] Attributes: [{self._attr_a}][{self._attr_b}]"


class ComponentD2(CompInterface):
    """Component Object --- Extended with an additional attribute (attr_c)"""

    def __init__(self, name: str, attr_a: str, attr_b: str, attr_c: str) -> None:
        self._name = name
        self._attr_a = attr_a
        self._attr_b = attr_b
        self._attr_c = attr_c

    def __repr__(self):
        return f"Component Class: [{self.__class__.__qualname__}] Category: [{self._name}] Attributes: [{self._attr_a}][{self._attr_b}][{self._attr_c}]"


# endregion


# region Builder


# Builder (Interface)
class Builder(ABC):
    """Interface for Concrete Builder"""

    def __init__(self, concrete_product: Type[Product] = ConcreteProductA):
        """Injects the Concrete Product. Inherited by Concrete Builder"""
        self._product: Product = concrete_product()

    @abstractmethod
    def build_component_a(self, component_obj: "CompInterface"):
        return self

    @abstractmethod
    def build_component_b(self, component_obj: "CompInterface"):
        return self

    @abstractmethod
    def build_component_c(self, component_obj: "CompInterface"):
        return self

    @abstractmethod
    def build_component_d(self, component_obj: "CompInterface"):
        return self

    def build(self) -> Product:
        """Needed to complete the build process - must run every time."""
        self._product.freeze()  # locks the product from further modification.
        return self._product


# Concrete Builder - Assembles the components together in various different configurations
# Requires Components of Type CompInterface
class ConcreteBuilderA(Builder):
    """Assembles the Final Product in a Unique Representation (ordering can change. Can leave out components if desired)"""

    def build_component_a(self, component_obj: "CompInterface"):
        self._product.set_component_a(component_obj)
        return self

    def build_component_b(self, component_obj: "CompInterface"):
        self._product.set_component_b(component_obj)
        return self

    def build_component_c(self, component_obj: "CompInterface"):
        self._product.set_component_c(component_obj)
        return self

    def build_component_d(self, component_obj: "CompInterface"):
        self._product.set_component_d(component_obj)
        return self


# endregion


# Director (Optional)
class Director:
    """Choose from specific preconfigured build order setups"""

    def __init__(self, concrete_builder: Builder) -> None:
        self._builder = concrete_builder

        # Map config keys to builder methods -- allow dynamic method lookup, so Director() can build components based on config without many if statements.
        self._component_map = {
            "ComponentA": self._builder.build_component_a,
            "ComponentB": self._builder.build_component_b,
            "ComponentC": self._builder.build_component_c,
            "ComponentD": self._builder.build_component_d,
        }

    def build_mvp(self):
        """Creates a minimal Build (with 2 components)"""
        return (
            self._builder.build_component_a(
                ComponentA("Comp A: name", "Comp A: attribute A", "Comp A: attribute B")
            )
            .build_component_b(
                ComponentB("Comp B: name", "Comp B: attribute A", "Comp B: attribute B")
            )
            .build()
        )

    def build_full_product(self):
        """Creates a complete build with all the components"""
        return (
            self._builder.build_component_a(
                ComponentA("Comp A: name", "Comp A: attribute A", "Comp A: attribute B")
            )
            .build_component_b(
                ComponentB("Comp B: name", "Comp B: attribute A", "Comp B: attribute B")
            )
            .build_component_c(
                ComponentC("Comp C: name", "Comp C: attribute A", "Comp C: attribute B")
            )
            .build_component_d(
                ComponentD("Comp D: name", "Comp D: attribute A", "Comp D: attribute B")
            )
            .build()
        )

    def build_from_config(self, config: dict) -> Product:
        """Builds a product using a Configuration Dictionary."""
        for label, component in config.items():
            selector = self._component_map.get(label)
            if not selector:
                raise ValueError(
                    f"Component Type: {label} is not valid. Available Components are {self._component_map.keys()}"
                )
            selector(component)  # unpacks attribute parameters
        return self._builder.build()


# --- Client Facing Code Usage ---
def main():

    # Manual Builder
    concrete_product_b = (
        ConcreteBuilderA(ConcreteProductB)
        .build_component_a(ComponentA(name="A", attr_a="Attribute A", attr_b="Attribute B"))
        .build_component_b(ComponentD2(name="B", attr_a="Attribute A", attr_b="Attribute B", attr_c="Attribute C"))
        .build()
    )
    # lists all the components the Object has.
    list_components = concrete_product_b.list_components()

    # Retrieve a component from the Concrete Product.
    get_component = concrete_product_b.get_component(ComponentA)
    print(f"GET COMPONENT: {get_component}")

    # Director Builder
    build_mvp_product = Director(ConcreteBuilderA(ConcreteProductB)).build_mvp().list_components()
    build_full_product = (Director(ConcreteBuilderA(ConcreteProductB)).build_full_product().list_components())

    # Director Config Builder
    config: dict[str, "CompInterface"] = {
        "ComponentA": ComponentA("A","Attribute A","Attribute B"),
        "ComponentB": ComponentB("B","Attribute A","Attribute B"),
        "ComponentC": ComponentC("C","Attribute A","Attribute B"),
        "ComponentD": ComponentD("D","Attribute A","Attribute B"),
    }
    director = Director(ConcreteBuilderA()).build_from_config(config).list_components()


if __name__ == "__main__":
    main()
