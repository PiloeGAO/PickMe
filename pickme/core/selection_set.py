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
    def __init__(self, rig=None, id=0, name="", objects=[]) -> None:
        self._rig = rig
        self._selection_set_path = os.path.join(os.path.dirname(os.path.realpath(self._rig.path)), "selection_sets.json")

        self._id = id
        self._name = name
        self._objects = objects
    
    @staticmethod
    def create_set(rig, name="", objects=[]):
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
            objects=objects
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
        selection_set_file = os.path.join(os.path.dirname(os.path.realpath(rig.path)), "selection_sets.json")

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
                        name=data["name"],
                        objects=data["objects"]
                    )
                )

        return selections_sets
    
    @staticmethod
    def save_sets(rig):
        """Save selection sets to disk.

        Args:
            rig (class: Rig): Rig
        """
        selection_set_file = os.path.join(os.path.dirname(os.path.realpath(rig.path)), "selection_sets.json")

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
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
    
    @property
    def objects(self):
        return self._objects
    
    @property
    def json(self):
        datas = {
            "id":self._id,
            "name":self._name,
            "objects":self._objects
        }

        return datas
    
    def select_objects(self):
        self._rig.manager.integration.select_objects(self._objects)