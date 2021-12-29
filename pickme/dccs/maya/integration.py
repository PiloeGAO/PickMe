'''
    :package:   PickMe
    :file:      integration.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Maya integration class.
'''
from maya import cmds
from maya.api import OpenMaya

from pickme.core.integration import Integration

class MayaIntegration(Integration):
    def __init__(self, manager=None) -> None:
        super(MayaIntegration, self).__init__()
        self._name = "Maya"
        self._manager = manager

        # Adding callbacks
        OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterCreateReference, self._manager.ui.reload_configurations)
        OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterRemoveReference, self._manager.ui.reload_configurations)
    
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

        if(len([ref for ref in loaded_references if f"{name}RN" in ref]) > 0):
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
            object_name = cmds.referenceQuery(ref, nodes=True)[0]
            object_name = object_name.split(":")[:-1][0]
            rigs_objects.append(object_name)

        return rigs_objects
    
    def get_selection(self):
        """Get the viewport selection.

        Returns:
            list: Object names
        """
        selection = [obj.replace(f"{self._manager.rig.name}:", "") for obj in cmds.ls(sl=True)]
        return selection
    
    def select_objects(self, objects, clear_selection=True):
        """Select the list of objects.

        Args:
            objects (list): Object names
        """
        cmds.select(clear=clear_selection)

        objects = [f"{self._manager.rig.name}:{obj}" for obj in objects]

        cmds.select(objects)
    
    def reset_moves(self, objects):
        """Reset the translation, position and scale of selection.

        Args:
            objects (list): Object names
        """
        objects = [f"{self._manager.rig.name}:{obj}" for obj in objects]

        for object in objects:
            if(not True in (cmds.getAttr(f"{object}.translate", lock=True), not cmds.getAttr(f"{object}.translate", settable=True))):
                cmds.setAttr(f"{object}.translate", 0, 0, 0)
            if(not True in (cmds.getAttr(f"{object}.rotate", lock=True), not cmds.getAttr(f"{object}.rotate", settable=True))):
                cmds.setAttr(f"{object}.rotate", 0, 0, 0)
            if(not True in (cmds.getAttr(f"{object}.scale", lock=True), not cmds.getAttr(f"{object}.scale", settable=True))):
                cmds.setAttr(f"{object}.scale", 1, 1, 1)