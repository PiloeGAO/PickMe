'''
    :package:   PickMe
    :file:      integration.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Default integration class.
'''

class Integration(object):
    def __init__(self):
        self._name = "Standalone"
    
    @property
    def name(self):
        return self._name
    
    def is_rig(self, name):
        """Check if the rig is loaded in the scene.

        Args:
            name (str): Name of the object

        Raises:
            RuntimeError: Only strings can be used

        Returns:
            bool: Is rig in the scene
        """
        if(type(name) != str):
            raise RuntimeError("Only strings can be used in the function.")
        
        return True
    
    def all_rigs(self, name):
        """Return a list of objects names.

        Returns:
            list: Names
        """
        return [name]