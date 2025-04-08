from enum import Enum
from aenum import extend_enum

def enum_extend_decorator(parent_enum: Enum):
    """Add the enum constant from parent enum to enum where is defined
    
    Args:
        - parent_enum (Enum): the enum where the constant will be extracted
    
    Returns:
        - function: the wrapper
    """

    def __extract_enum_name_value__(name, obj_value):
        """Get the value of enum constant value

        Args:
            - name (string): the constant name
            - obj_value (property_enum): the value related to enum constant

        Returns:
            - string: the constant name
            - any: the value related to constant
        """
        return name, obj_value.value


    def wrapper(added_enum):
        """Extend the enum with parent constants

        Args:
            - added_enum (Enum): the enum to extend

        Returns:
            - Enum: the extended enum
        """
        parent_constants = list(map(lambda item: __extract_enum_name_value__(*item),
                                    parent_enum._member_map_.items()))
        for name, value in parent_constants:
            extend_enum(added_enum, name, value)
        return added_enum
    
    return wrapper
