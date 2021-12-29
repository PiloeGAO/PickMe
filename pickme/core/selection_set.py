'''
    :package:   PickMe
    :file:      selection_set.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Selection Set Management class.
'''
import os
import json

class SelectionSet():
    def __init__(self, rig=None, id=0, name="", objects=[], color="", icon="") -> None:
        self._rig = rig
        self._rig_config_path = self._rig.path
        self._selection_set_path = os.path.join(self._rig_config_path, "selection_sets.json")

        self._id = id
        self._name = name
        self._objects = objects
        self._color  = color
        self._icon = icon
    
    @staticmethod
    def create_set(rig, name="", objects=[], icon=""):
        """Create a new selection set.

        Args:
            rig (class: Rig): Rig

        Returns:
            list: Selection sets
        """
        selection_sets = rig.selection_sets

        new_set = SelectionSet(
            rig,
            id=len(selection_sets),
            name=name,
            objects=objects,
            icon=icon
        )
        
        selection_sets.append(new_set)
        return selection_sets
    
    @staticmethod
    def load_sets(rig):
        """Create Selection sets from a filepath.

        Args:
            rig (class: Rig): Rig Class

        Returns:
            list: Selection sets for the given rig
        """
        selection_set_file = os.path.join(rig.path, "selection_sets.json")

        if(not os.path.isfile(selection_set_file)):
            return []
        
        selections_sets = []

        with open(selection_set_file, "r+") as file:
            datas = json.loads(file.read())

            for data in datas:
                selections_sets.append(
                    SelectionSet(
                        rig=rig, 
                        id=data["id"],
                        name=data.get("name", "Selection Set"),
                        objects=data.get("objects",[]),
                        color=data.get("color", ""),
                        icon=data.get("icon", "")
                    )
                )

        return selections_sets
    
    @staticmethod
    def save_sets(rig):
        """Save selection sets to disk.

        Args:
            rig (class: Rig): Rig
        """
        selection_set_file = os.path.join(rig.path, "selection_sets.json")

        if(not os.path.isfile(selection_set_file)):
            file = open(selection_set_file, "w")
            file.write("[]")
            file.close()

        with open(selection_set_file, "r+") as file:
            content = []

            for set in rig.selection_sets:
                content.append(set.json)

            file.seek(0)
            file.write(json.dumps(content, indent=4))
            file.truncate()

    @property
    def rig(self):
        return self._rig

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def objects(self):
        return self._objects
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, new_color):
        self._color = new_color
    
    @property
    def icon(self):
        return os.path.join(self._rig_config_path, "icons", self._icon)
    
    @property
    def icon_name(self):
        return self._icon
    
    @icon.setter
    def icon(self, icon):
        self._icon = icon
    
    @property
    def json(self):
        """Convert the class to json formating.

        Returns:
            dict: Parsed data
        """
        datas = {
            "id": self._id,
            "name": self._name,
            "objects": self._objects,
            "color": self._color,
            "icon": self._icon
        }

        return datas
    
    def select_objects(self):
        """Select objects (shortcut to the integration).
        """
        self._rig.manager.integration.select_objects(self._objects)
    
    def reset_moves(self):
        """Reset the pos-rot-scale of the selection (shortcut to the integration).
        """
        self._rig.manager.integration.reset_moves(self._objects)