from typing import Any


# Registry Class
# only stores Classes at the moment - change type if you want to store other objects.
class Registry:
    def __init__(self) -> None:
        self._store: dict[str, type] = {}

    def register(self, label: str, cls:type) -> None:
        if label in self._store:
            raise KeyError(f"'{label}' is already registered...")
        self._store[label] = cls

    def get(self, label: str) -> type:
        if label not in self._store:
            raise ValueError(f"'{label}' not found. Available: {list(self._store.keys())}")
        return self._store.get(label)   # type: ignore

    def display_items(self):
        print(f"\nRegistry Contains the Following Items:\n")
        for label, cls in self._store.items():
            print(f"Registry Item Label: {label} | Class: {cls.__qualname__} | Memory Address: {hex(id(cls))}")


# Dummy Class Examples
class ClassA:
    def __init__(self) -> None:
        pass


class ClassB:
    def __init__(self) -> None:
        pass


class ClassC:
    def __init__(self) -> None:
        pass


# --- Client Facing Code ---
register = Registry()

# add a new class to the registry
register.register("Class A", ClassA)
register.register("Class B", ClassB)
register.register("Class C", ClassC)

# Collect a class from the registry
class_A = register.get("Class A")
print(f"Class: {class_A.__qualname__} at {hex(id(class_A))}")

# instantiate class
class_A = class_A()
print(class_A)


# Display all Items in the registry
register.display_items()
