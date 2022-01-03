'''
    :package:   PickMe
    :file:      integration.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Default integration class.
'''

class Integration(object):
    def __init__(self, manager=None):
        self._name = "Standalone"
        self._manager = manager
    
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
    
    def get_selection(self):
        """Get the viewport selection.

        Returns:
            list: Object names
        """
        return ["Toto"]
    
    def select_objects(self, objects):
        """Select the list of objects.

        Args:
            objects (list): Object names
        """
        print(objects)
    
    def reset_moves(self, objects):
        """Reset the translation, position and scale of selection.

        Args:
            objects (list): Object names
        """
        print(f"Reset {objects}")
    
    def update_attribute(self, attribute):
        """Update attribute for object.

        Args:
            attribute (class: Attribute): Attribute
        """
        print(f"Updating {attribute.object} > {attribute.name} to {attribute.value}")