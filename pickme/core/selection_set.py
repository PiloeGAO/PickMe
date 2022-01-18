'''
    :package:   PickMe
    :file:      selection_set.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Selection Set Management class.
'''
import os
import uuid
import json


class SelectionSetManager():
    def __init__(self, path, rig, is_editable=True) -> None:
        self.id = uuid.uuid4()
        self._rig = rig
        self._path = path
        self._is_editable = is_editable
        self._selection_sets = []

        self.load_sets()
    
    @property
    def rig(self):
        return self._rig
    
    @property
    def selection_sets(self):
        return self._selection_sets
    
    @property
    def is_editable(self):
        return self._is_editable

    def create_selection_set(self, name="", objects=[], icon="", color=""):
        """Create a new selection set.

        Args:
            name (str, optional): Name. Defaults to "".
            objects (list, optional): Objects inside of it. Defaults to [].
            icon (str, optional): icon of the set. Defaults to "".
            color (str, optional): color of the set. Defaults to "".
        """
        new_set = SelectionSet(
            self,
            id=len(self._selection_sets),
            name=name,
            objects=objects,
            icon=icon,
            color=color
        )
        
        self._selection_sets.append(new_set)
    
    def delete_selection_set(self, id):
        """Delete the selection set for the given id.

        Args:
            id (int): ID of the selection set
        """
        if(not self._is_editable): return

        to_del_position = -1
        for i, selection_set in enumerate(self._selection_sets):
            if(selection_set.id == id and to_del_position == -1):
                to_del_position = i
                continue
                
            if(selection_set.id > id):
                selection_set.id -= 1

        del self._selection_sets[to_del_position]

        self.save_sets()

    def load_sets(self):
        """Create Selection sets from a filepath.

        Returns:
            list: Selection sets for the given rig
        """
        self._selection_sets = []

        if(not os.path.isfile(self._path)):
            return

        with open(self._path, "r+") as file:
            datas = json.loads(file.read())

            for data in datas:
                self._selection_sets.append(
                    SelectionSet(
                        self, 
                        id=data["id"],
                        name=data.get("name", "Selection Set"),
                        objects=data.get("objects",[]),
                        color=data.get("color", ""),
                        icon=data.get("icon", "")
                    )
                )
    
    def save_sets(self):
        """Save selection sets to disk.
        """
        if(not os.path.isdir(os.path.dirname(self._path))):
            # Create the directory if needed.
            os.mkdir(os.path.dirname(self._path))

        if(not os.path.isfile(self._path)):
            # Write the file if it not exist.
            file = open(self._path, "w")
            file.write("[]")
            file.close()

        with open(self._path, "r+") as file:
            content = []

            for selection_set in self._selection_sets:
                content.append(selection_set.json)

            file.seek(0)
            file.write(json.dumps(content, indent=4))
            file.truncate()

class SelectionSet():
    def __init__(self, selection_set_manager, id=0, name="", objects=[], color="", icon="") -> None:
        self._selection_set_manager = selection_set_manager

        self._id = id
        self._name = name
        self._objects = objects
        self._color  = color
        self._icon = icon
    
    @property
    def selection_set_manager(self):
        return self._selection_set_manager

    @property
    def rig(self):
        return self.selection_set_manager.rig

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
        return os.path.join(self.rig.path, "icons", self._icon)
    
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
        self.rig.manager.integration.select_objects(self._objects)
    
    def reset_moves(self):
        """Reset the pos-rot-scale of the selection (shortcut to the integration).
        """
        self.rig.manager.integration.reset_moves(self._objects)