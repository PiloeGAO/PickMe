'''
    :package:   PickMe
    :file:      rig.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Rig Management class.
'''
import os
import json

class Rig():
    def __init__(self, id=-1, name="Default", path=None, icon=None) -> None:
        self._id = id
        self._name = name
        self._path = path
        self._icon = icon
        self._selection_set_path = os.path.join(os.path.dirname(os.path.realpath(path)), "selection_sets.json")
        self._selection_sets = self.load_selection_sets()
    
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
    
    @property
    def icon(self):
        return self._icon
    
    @property
    def selection_sets(self):
        return self._selection_sets
    
    def reload(self):
        """Force rig class reload.
        """
        self._selection_sets = self.load_selection_sets()

    def load_selection_sets(self):
        """Load the content of the selection set from disk.

        Returns:
            list: Selections sets
        """
        if(not os.path.isfile(self._selection_set_path)):
            return []
        
        with open(self._selection_set_path, "r+") as file:
            return json.loads(file.read())

    def create_selection_set(self, name, objects):
        """Create selection set and them it to disk.

        Args:
            name (str): Name of the set
            objects (list): Objects name
        """
        if(not os.path.isfile(self._selection_set_path)):
            file = open(self._selection_set_path, "w")
            file.write("[]")
            file.close()
        
        with open(self._selection_set_path, "r+") as file:
            content = json.loads(file.read())

            content.append(
                {
                    "id":len(content),
                    "name":name,
                    "objects":objects
                }
            )

            file.seek(0)
            file.write(json.dumps(content))
            file.truncate()

            self._selection_sets = content