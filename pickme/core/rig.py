'''
    :package:   PickMe
    :file:      rig.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Rig Management class.
'''
import os
import json

from pickme.core.attribute import AttributeGroup, Attribute
from pickme.core.exceptions import CoreError
from pickme.core.path import GLOBAL_CONFIG_DIR, LOCAL_CONFIG_DIR
from pickme.core.picker import PickerCore
from pickme.core.selection_set import SelectionSetManager
from pickme.core.svg import SVGDocument

from pickme.core.logger import get_logger
logger = get_logger()

class Rig():
    def __init__(self, manager=None, id=-1, name="Default", path=None) -> None:
        self._manager = manager

        self._id = id
        self._name = name
        self._path = path
        self._config_path = os.path.join(path, "config.json")
        self._icon = os.path.join(path, "icon.png")

        self._picker_groups = []
        self._current_picker_group = 0
        self.load_picker_groups()

        self._selection_sets_managers = []
        self.load_selection_sets()

        self._attributes = []

        self._custom_rig_objects = []
        self.load_rig_objects()

    @classmethod
    def create(cls, manager, name):
        """Create a new rig from the manager and a rig name.

        Args:
            manager (:obj:`pickme.core.manager.Manager`): PickMe Manager
            name (str): Name of the rig

        Returns:
            :obj:`pickme.core.rig.Rig`: New rig
        """
        if(name in [rig.name for rig in manager.rigs]):
            return None

        path = os.path.join(GLOBAL_CONFIG_DIR, name)
        if(not os.path.isdir(path)): os.mkdir(path)

        config_file = os.path.join(path, "config.json")
        if(not os.path.isfile(config_file)):
            # Write the file if it not exist.
            file = open(config_file, "w")
            file.write("[]")
            file.close()

        return cls(manager=manager, name=name, path=path)
    
    @property
    def manager(self):
        return self._manager

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
    
    @property
    def path(self):
        return self._path

    @property
    def icon(self):
        return self._icon
    
    @property
    def picker_groups(self):
        return self._picker_groups
    
    @property
    def current_picker_group(self):
        if(len(self._picker_groups) > 0):
            return self._picker_groups[self._current_picker_group]
        
        raise CoreError(f"No picker group loaded in {self._name}.")
    
    @current_picker_group.setter
    def current_picker_group(self, picker_group):
        group_index = self._picker_groups.index(picker_group)

        if(group_index >= 0):
            self._current_picker_group = group_index
        else:
            raise CoreError(f"No picker group {picker_group.name} in {self.name}.")
    
    @property
    def selection_sets(self):
        selection_sets = []
        for selection_set_manager in self._selection_sets_managers:
            selection_sets.extend(selection_set_manager.selection_sets)
        
        return selection_sets
    
    @property
    def attributes(self):
        return self._attributes
    
    @attributes.setter
    def attributes(self, attributes=[]):
        if(type(attributes) != list):
            raise TypeError("attributes property can only be set with a list")
        
        self._attributes = attributes
    
    # Pickers Groups.
    def load_picker_groups(self):
        """Load picker groups from disk.
        """
        self._picker_groups = []

        picker_layers_directory = os.path.join(self._path, "layers")
        if(not os.path.isdir(picker_layers_directory)):
            logger.info("No pickers layers directory, creating one.")
            os.mkdir(picker_layers_directory)
            return

        for file in os.listdir(picker_layers_directory):
            if(not os.path.splitext(file)[1] in (".svg")):
                continue

            self._picker_groups.append(
                PickerCore.create(
                    os.path.join(picker_layers_directory, file),
                    manager=self._manager
                )
            )
    
    def create_picker_group(self, name, *args, **kwargs):
        """Create a new picker group.

        Args:
            name (str): Name fo the group

        Raises:
            CoreError: File with same name already exist
        """
        name = name.replace(" ", "_")
        svg_path = os.path.join(self._path, "layers", f"{name}.svg")
        
        if(os.path.isfile(svg_path)):
            raise CoreError("SVG Layer file already exist.")

        new_picker = SVGDocument.create(svg_path)
        new_picker.width = kwargs.get("width", 512)
        new_picker.height = kwargs.get("height", 512)
        new_picker.save(force_write=True)

        self.load_picker_groups()
        self._current_picker_group = len(self._picker_groups)-1
    
    def set_current_picker_group(self, picker_group):
        """Utils function to allow partial to edit the property.

        Args:
            picker_group (:obj:`pickme.core.picker.PickerCore`): New picker group to apply
        """
        self.current_picker_group = picker_group
        
        self._manager.ui.pickerWidget.load_picker()
        
    # Selection Sets.
    def load_selection_sets(self):
        self._selection_sets_managers.append(
            SelectionSetManager(
                os.path.join(self._path, "selection_sets.json"),
                self,
                is_editable=False
            )
        )

        self._selection_sets_managers.append(
            SelectionSetManager(
                os.path.join(LOCAL_CONFIG_DIR, self.name, "selection_sets.json"),
                self
            )
        )

    def create_selection_set(self, name, objects, icon, color="#0a3d62"):
        """Create selection set and them it to disk.

        Args:
            name (str): Name of the set
            objects (list): Objects name
        """
        self._selection_sets_managers[1].create_selection_set(
            name=name,
            objects=objects,
            icon=icon,
            color=color
        )

        self._selection_sets_managers[1].save_sets()

    def delete_selection_set(self, manager, id):
        """Delete a selection set.
        """
        manager.delete_selection_set(id)
        manager.save_sets()

    def save_selection_sets(self):
        """Save selections sets to disk.
        """
        for selection_set_manager in self._selection_sets_managers:
            selection_set_manager.save_sets()
    
    def reload(self):
        """Force rig class reload.
        """
        for selection_set_manager in self._selection_sets_managers:
            selection_set_manager.load_sets()
    
    def show_hide_selection_set(self, selection_set):
        """Show/hide selection set.

        Args:
            selection_set (:obj:`pickme.core.selection_set.SelectionSet`): Set to show/hide
        """
        objects = selection_set.objects
        self._manager.integration.show_hide_objects(objects)
    
    # Rig Objects management.
    @property
    def rig_objects(self):
        return self._custom_rig_objects

    def load_rig_objects(self):
        """Load rig objects stored in the config.
        """
        if(not os.path.isfile(self._config_path)):
            return

        def recursive_attribute_load(elem, parent):
            """Recursively load attributes/attributes groups.

            Args:
                elem (str): JSON Datas
                parent (:obj:`pickme.core.attribute.AttributeGroup`): [description]
            """
            if(elem.get("childs", None) != None):
                group = AttributeGroup(
                    self,
                    elem["object"],
                    elem["name"]
                )

                parent.add_child(group)

                for sub_elem in elem:
                    recursive_attribute_load(sub_elem, group)
            
            else:
                parent.add_child(
                    Attribute(
                        self,
                        elem["object"],
                        elem["name"],
                        elem["attribute_type"],
                        elem["default_value"],
                        min_value=elem["min_value"],
                        max_value=elem["max_value"],
                        enum_list=elem["enum_list"]
                    )
                )

        with open(self._config_path, "r+") as file:
            datas = json.loads(file.read())

            for data in datas:
                name = data["name"]
                attributes = []

                for attribute_group in data["attributes"]:
                    group = AttributeGroup(
                        self,
                        attribute_group["object"],
                        attribute_group["name"]
                    )

                    attributes.append(group)

                    for sub_elem in attribute_group["childs"]:
                        recursive_attribute_load(sub_elem, group)

                self._custom_rig_objects.append(
                    RigObject(
                        name,
                        attributes
                    )
                )

    def save_rig_objects(self):
        """Save the list of custom rig objects on disk.
        """
        if(not os.path.isdir(os.path.dirname(self._config_path))):
            # Create the directory if needed.
            os.mkdir(os.path.dirname(self._config_path))

        if(not os.path.isfile(self._config_path)):
            # Write the file if it not exist.
            file = open(self._config_path, "w")
            file.write("[]")
            file.close()

        with open(self._config_path, "r+") as file:
            content = []

            for rig_obj in self._custom_rig_objects:
                content.append(rig_obj.json)

            file.seek(0)
            file.write(json.dumps(content, indent=4))
            file.truncate()
    
    def create_custom_rig_object(self, name, attributes):
        """Add a new custom rig object.

        Args:
            name (str): Object name
            attributes (list: :obj:`pickme.core.attribute.BaseAttribute`): List of attributes
        """
        self._custom_rig_objects.append(
            RigObject(
                name,
                attributes
            )
        )

        self.save_rig_objects()

class RigObject:
    def __init__(self, name, attributes=[]):
        """Create a RigObject class instance.

        Args:
            name (str): Name of the 3D Object
            attributes (list: :obj:`pickme.core.attribute.BaseAttribute`, optional): List of attributes for the object. Defaults to [].
        """
        self._name = name
        self._attributes = attributes
    
    @property
    def json(self):
        return {
            "name": self._name,
            "attributes": [attr.json for attr in self._attributes]
        }

    @property
    def name(self):
        return self._name

    @property
    def attributes(self):
        return self._attributes