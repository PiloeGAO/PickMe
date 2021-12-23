'''
    :package:   PickMe
    :file:      rig.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Rig Management class.
'''

class Rig():
    def __init__(self, name="Default", path=None, icon=None) -> None:
        self._name = name
        self._path = path
        self._icon = icon
    
    @property
    def name(self):
        return self._name
    
    @property
    def icon(self):
        return self._icon