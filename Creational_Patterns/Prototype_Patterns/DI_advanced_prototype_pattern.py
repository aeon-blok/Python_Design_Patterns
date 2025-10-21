import copy
from typing import Any, Dict, Optional


# Prototype
class Prototype:
    """
    - Dependency Injection Based Prototype Cloner
    - Shallow & Deep Copying via Parameter
    - Selective Cloning via (Inclusion & Exclusion Lists)
    - Attribute Overrides via **Kwargs
    """

    def __init__(self, obj: object, copy_type=copy.deepcopy) -> None:
        self._obj = obj
        self._copy = copy_type

    def clone(
        self,
        include: Optional[list[str]] = None,
        exclude: Optional[list[str]] = None,
        **attribute_overrides
    ) -> object:

        #  STEP 1: Attribute Overrides
        obj_attributes = self._copy(self._obj.__dict__)  # deep copy Object attributes
        # apply Attribute Overrides to the Object __dict__ (stores all object attributes)
        obj_attributes.update(attribute_overrides)

        # STEP 2: Inclusion List
        if include:
            obj_attributes = {k: v for k, v in obj_attributes.items() if k in include}

        # STEP 3: Exclusion List
        if exclude:
            obj_attributes = {k: v for k, v in obj_attributes.items() if not k in exclude}

        # STEP 4: Copys Concrete prototype and creates a new instance.
        clone = type(self._obj).__new__(type(self._obj))
        # apply attribute overrides to the new copy.
        clone.__dict__.update(obj_attributes)

        return clone


# Concrete Prototype
class Target:
    def __init__(self, attr_a, attr_b, attr_c) -> None:
        self._attr_a = attr_a
        self._attr_b = attr_b
        self._attr_c = attr_c

    @property
    def attr_a(self):
        return self._attr_a

    @property
    def attr_b(self):
        return self._attr_b

    @property
    def attr_c(self):
        return self._attr_c


# Client facing Code
# Main
def main():

    # Setup Concrete Prototype
    test_class = Target("Attribute A", "Attribute B", "Attribute C")

    # Run Prototype Logic
    clone = Prototype(test_class).clone(_attr_a="Attribute D")

    # Check attribute override
    print(clone.attr_a) # type: ignore


if __name__ == "__main__":
    main()

