'''
    :package:   PickMe
    :file:      picker.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     Picker class.
'''
import os

class Picker:
    def __init__(self, name, description, buttons=[]) -> None:
        self._name = name
        self._description = description
        self._buttons = buttons
    
    @classmethod
    def create(cls, path):
        """Create the Picker Object from a path.

        Args:
            path (str): Path to SVG file

        Returns:
            class: Picker: Picker object
        """
        name = os.path.splitext(path)[0] # TODO: Use the name stored in the SVG.
        description = "" # TODO: Use the description stored in the metadatas of the SVG.
        buttons = []
        return cls(name, description, buttons)

    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def buttons(self):
        return self._buttons