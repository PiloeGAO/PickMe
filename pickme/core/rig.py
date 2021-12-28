'''
    :package:   PickMe
    :file:      rig.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Rig Management class.
'''
import os
import json

from pickme.core.selection_set import SelectionSet

class Rig():
    def __init__(self, manager=None, id=-1, name="Default", path=None, icon=None) -> None:
        self._manager = manager

        self._id = id
        self._name = name
        self._path = path
        self._icon = icon
        self._selection_sets = SelectionSet.load_sets(self)
    
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
    def selection_sets(self):
        return self._selection_sets
    
    def reload(self):
        """Force rig class reload.
        """
        self._selection_sets = SelectionSet.load_sets(self)

    def create_selection_set(self, name, objects):
        """Create selection set and them it to disk.

        Args:
            name (str): Name of the set
            objects (list): Objects name
        """
        self._selection_sets = SelectionSet.create_set(self, name=name, objects=objects)
        self.save_selection_sets()

    def delete_selection_set(self, id):
        """Delete a selection set.
        """
        for selection_set in self._selection_sets:
            if(selection_set.id > id):
                selection_set.id -= 1

        del self._selection_sets[id]
        
        self.save_selection_sets()

    def save_selection_sets(self):
        """Save selections sets to disk.
        """
        SelectionSet.save_sets(self)