'''
    :package:   PickMe
    :file:      attribute.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     Attribute class.
'''

from pickme.core.exceptions import CoreError

class AttributeTypes():
    none = -1
    group = 0
    number = 1 # Can be int or float
    boolean = 2
    string = 3
    enum = 4

class BaseAttribute:
    def __init__(self, rig, object, name):
        self._rig  = rig
        self._object = object
        self._attribute_type = AttributeTypes.none
        self._name = name
        self._nice_name = self._name
    
    @property
    def attribute_type(self):
        return self._attribute_type

    @property
    def object(self):
        return self._object

    @property
    def name(self):
        return self._name
    
    @property
    def nice_name(self):
        nice_name_with_space = self._nice_name.replace("_", " ")
        return "".join(map(lambda x: x if x.islower() else " "+x, nice_name_with_space))

class AttributeGroup(BaseAttribute):
    def __init__(self, rig, object, name):
        super().__init__(rig, object, name)
        
        self._attribute_type = AttributeTypes.group

        self._childs = []
    
    @property
    def childs(self):
        return self._childs
    
    @childs.setter
    def childs(self, childs):
        self._childs = childs
    
    def add_child(self, new_attribute):
        new_attribute.parent_attribute = self
        self._childs.append(new_attribute)

class Attribute(BaseAttribute):
    def __init__(self, rig, object, name, attribute_type, default_value, parent_attribute=None, **kwargs):
        super(Attribute, self).__init__(rig, object, name)
        self._parent_attribute = parent_attribute
        
        if(type(parent_attribute) == AttributeGroup):
            self._nice_name = self._nice_name.replace(parent_attribute.name, "")

        self._attribute_type = attribute_type
        self._default_value = default_value
        self._value = default_value

        self._min_value = kwargs.get("min_value", 0)
        self._max_value = kwargs.get("max_value", 1)

        if(kwargs.get("enum_list", None) != None):
            self._enum_list = kwargs.get("enum_list")
    
    @property
    def parent_attribute(self):
        return self._parent_attribute
    
    @parent_attribute.setter
    def parent_attribute(self, new_parent):
        self._parent_attribute = new_parent

        if(type(new_parent) == AttributeGroup):
            self._nice_name = self._nice_name.replace(new_parent.name, "")

    @property
    def default_value(self):
        return self._default_value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        """Set the value of the attribute.

        Args:
            value (int, float, bool, str): The value to set

        Raises:
            CoreError: If the AttributeType is a number, the value must be a number.
            CoreError: If the AttributeType is a boolean, the value must be a boolean.
            CoreError: If the AttributeType is a string, the value must be a string.
        """
        if(self._attribute_type == AttributeTypes.number and not type(value) in (int, float)):
            raise CoreError(f"The value [{value}] must be a number.")
        elif(self._attribute_type == AttributeTypes.boolean and not type(value) in (bool, int)):
            raise CoreError(f"The value [{value}] must be a boolean.")
        elif(self._attribute_type == AttributeTypes.string and not type(value) == str):
            raise CoreError(f"The value [{value}] must be a string.")
        elif(self._attribute_type == AttributeTypes.enum and not type(value) == int):
            raise CoreError(f"The value [{value}] must be a list of strings.")
        
        self._value = value
    
    @property
    def min_value(self):
        return self._min_value
    
    @property
    def max_value(self):
        return self._max_value
    
    @property
    def enum_list(self):
        return self._enum_list
    
    def edit_attribute(self, value):
        """Update the attribute class and push modification to the integration.

        Args:
            value (int, float, bool, str): New value to apply
        """
        self.value = value
        self._rig.manager.integration.update_attribute(self)