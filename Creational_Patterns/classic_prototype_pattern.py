import copy


# Prototype (Key Component of the Prototype Pattern)
class Prototype:
    """Clones an Exisiting Class, with the ability to Include and Exclude Specific User Defined Attributes."""

    def filter_attributes(self, include=None, exclude=None):
        """Helper Method - Logic For Inclusion & Exclusion lists. Can Exclude or Whitelist Attributes to clone from the original class."""
        clone = copy.deepcopy(self)
        attributes = set(vars(clone).keys())  # all the current attributes in a set{}

        if include is not None:
            # keeps attributes on the include list and removes the rest.
            delete_list = attributes - set(include)  
        elif exclude is not None:
            # Set Intersection - keeps items on the exclude list to delete.
            delete_list = (set(exclude) & attributes)  
        else:
            delete_list = set()

        for attribute in delete_list:
            delattr(clone, attribute)
        return clone

    def clone(self, include=None, exclude=None):
        return self.filter_attributes(include=include, exclude=exclude)


# Concrete Prototype (inherits from prototype) -- this is your target class. (can be anything)
class Target(Prototype):
    def __init__(self, attr_a, attr_b, attr_c, attr_d):
        self._attr_a = attr_a
        self._attr_b = attr_b
        self._attr_c = attr_c
        self._attr_d = attr_d

    @property
    def attr_a(self):
        return self._attr_a

    @property
    def attr_b(self):
        return self._attr_b

    @property
    def attr_c(self):
        return self._attr_c

    @property
    def attr_d(self):
        return self._attr_d


# Main
def main():

    # create target class instance
    test_class = Target("Attribute A", "Attribute B", "Attribute C", "Attribute D")

    # Clone Instance
    clone = test_class.clone()

    # needs to be the actual attribute name not a getter property
    include_list_clone = test_class.clone(include=["_attr_a"]) 

    # needs to be the actual attribute name not a getter property
    exclude_list_clone = test_class.clone(exclude=["_attr_a"])  

    # Check they are different objects.
    print(f"Object: {test_class.__class__.__qualname__} at Memory Address: {hex(id(test_class))}")
    print(f"Object: {clone.__class__.__qualname__} at Memory Address: {hex(id(clone))}")

    # check the attributes of the clone
    print(f"Clone: {clone.__class__.__qualname__}: {clone.attr_a}, {clone.attr_b}, {clone.attr_c}, {clone.attr_d}")

    # check the attributes of the clone via inclusion list. (will only have the attributes on the inclusion list.)
    print(
        f"Clone With Inclusion List: {include_list_clone.__class__.__qualname__}: {include_list_clone.attr_a}"
    )

    # check the attributes of the clone via exclusion list. (will only have the attributes NOT on the exclusion list)
    print(
        f"Clone With Exclusion List: {exclude_list_clone.__class__.__qualname__}: {exclude_list_clone.attr_b}, {exclude_list_clone.attr_c}, {exclude_list_clone.attr_d}"
    )


if __name__ == "__main__":
    main()
