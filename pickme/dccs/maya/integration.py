'''
    :package:   PickMe
    :file:      integration.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Maya integration class.
'''
from maya import cmds
from pickme.core.integration import Integration

class MayaIntegration(Integration):
    def __init__(self) -> None:
        super(MayaIntegration, self).__init__()

        self._name = "Maya"
    
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
        
        loaded_references = cmds.ls(references=True)

        if(f"{name}RN" in loaded_references):
            return True
        
        return False
    
    def all_rigs(self, name):
        """Return a list of objects names.

        Returns:
            list: Names
        """
        rigs_objects = []
        all_references = [ref for ref in cmds.ls(references=True) if f"{name}RN" in ref]

        for ref in all_references:
            rigs_objects.append(cmds.referenceQuery(ref, nodes=True)[0])

        return rigs_objects