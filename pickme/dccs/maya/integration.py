'''
    :package:   PickMe
    :file:      integration.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Maya integration class.
'''
from maya import cmds, utils
from maya.api import OpenMaya

from pickme.core.attribute import AttributeGroup, AttributeTypes, Attribute
from pickme.core.exceptions import CoreError
from pickme.core.integration import Integration

from pickme.core.logger import get_logger
logger = get_logger()

class MayaIntegration(Integration):
    def __init__(self, manager=None) -> None:
        super(MayaIntegration, self).__init__()
        self._name = "Maya"
        self._manager = manager

        # Adding callbacks
        OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterCreateReference, self._manager.ui.reload_configurations)
        OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterRemoveReference, self._manager.ui.reload_configurations)
        OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterLoadReference, self._manager.ui.reload_configurations)

        OpenMaya.MEventMessage.addEventCallback("SelectionChanged", self.get_attributes_for_selection)
        OpenMaya.MEventMessage.addEventCallback("timeChanged", self.refresh_attributes)
    
    def hook_exceptions(self):
        """Define a custom exception handling for the application.
        Source: https://around-the-corner.typepad.com/adn/2013/03/my-entry.html
        """
        old_hook = utils.formatGuiException

        def new_hook(type, value, traceback, detail):
            self._manager.error_exec_function(type, value, traceback)
            old_hook(type, value, traceback, detail)

            return utils._formatGuiException(type, value, traceback, detail)

        utils.formatGuiException = new_hook

    def is_rig(self, name):
        """Check if the rig is loaded in the scene.

        Args:
            name (str): Name of the object

        Raises:
            CoreError: Only strings can be used

        Returns:
            bool: Is rig in the scene
        """
        if(type(name) != str):
            raise CoreError("Only strings can be used in the function.")
        
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
    
    def get_rig_selected(self):
        """Get the name of the selected rig.

        Returns:
            str: Name of the reference.
        """
        selections = cmds.ls(sl=True)
        if(len(selections) != 1): return ""

        selection = selections[0]

        if(not "RN" in selection): return ""

        return selection.split("RN")[0]
    
    def select_objects(self, objects, clear_selection=True):
        """Select the list of objects.

        Args:
            objects (list): Object names
        """
        objects = [f"{self._manager.rig.name}:{obj}" for obj in objects if f"{self._manager.rig.name}:{obj}" in cmds.ls()]
        
        if(objects == []):
            return

        cmds.select(clear=clear_selection)
        cmds.select(objects)
    
    def show_hide_objects(self, objects):
        """Show/hide the list of objects

        Args:
            objects (list): Object names.
        """
        for obj in objects:
            new_visibility = not cmds.getAttr(f"{self._manager.rig.name}:{obj}.visibility")
            try:
                cmds.setAttr(f"{self._manager.rig.name}:{obj}.visibility", new_visibility)
            except Exception as e:
                logger.error(f"Failed to set visibility of {obj}")
    
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
    
    def get_attributes_for_selection(self, *args, **kwargs):
        """Get the attributes from the selection.
        """
        if(self._manager.rig == None): return

        attributes = []

        for sel in cmds.ls(sl=True, exactType="transform"):
            if(sel in [f"{self._manager.rig.name}:{obj.name}" for obj in self._manager.rig.rig_objects]):
                logger.debug(f"Loading custom rig object \"{sel}\" from the config.")
                # Load from custom rig object config.
                rig_object = [obj for obj in self._manager.rig.rig_objects if obj.name == sel.split(":")[-1]][0]

                attributes.extend(rig_object.attributes)

            else:
                logger.debug(f"Dynamicly building attributes for \"{sel}\".")
                # Dynamicly build attributes.
                attributes.append(
                    AttributeGroup(
                        self._manager.rig,
                        sel,
                        f"{sel}"
                    )
                )

                for attr in cmds.listAttr(sel, keyable=True):
                    maya_attribute_type = cmds.getAttr(f"{sel}.{attr}", type=True)

                    if(maya_attribute_type == "enum" and
                        cmds.attributeQuery(attr, node=sel, listEnum=True)[0] == "---------------"):
                        # Create group
                        attributes.append(
                            AttributeGroup(
                                self._manager.rig,
                                sel,
                                f"{attr}"
                            )
                        )
                        continue

                    # Create attributes.
                    attribute_name = attr
                    attribute_value = cmds.getAttr(f"{sel}.{attr}")

                    if(maya_attribute_type in ("double", "long")):
                        if(cmds.attributeQuery(attr, node=sel, minExists=True)):
                            attribute_min = cmds.attributeQuery(attr, node=sel, min=True)[0]
                        else:
                            attribute_min = attribute_value * -2
                            
                        if(cmds.attributeQuery(attr, node=sel, maxExists=True)):
                            attribute_max = cmds.attributeQuery(attr, node=sel, max=True)[0]
                        else:
                            attribute_max = attribute_value * 2
                    
                        new_attribute = Attribute(
                            self._manager.rig,
                            sel,
                            attribute_name,
                            AttributeTypes.number,
                            attribute_value,
                            min_value = attribute_min,
                            max_value = attribute_max
                        )

                    elif(maya_attribute_type == "bool"):
                        new_attribute = Attribute(
                            self._manager.rig,
                            sel,
                            attribute_name,
                            AttributeTypes.boolean,
                            attribute_value
                        )
                    
                    elif(maya_attribute_type == "enum"):
                        enum_values = cmds.attributeQuery(attr, node=sel, listEnum=True)[0].split(":")
                    
                        new_attribute = Attribute(
                            self._manager.rig,
                            sel,
                            attribute_name,
                            AttributeTypes.enum,
                            attribute_value,
                            enum_list = enum_values
                        )
                        
                    else:
                        attribute_value = str(attribute_value)
                    
                        new_attribute = Attribute(
                            self._manager.rig,
                            sel,
                            attribute_name,
                            AttributeTypes.string,
                            attribute_value
                        )

                    attributes[-1].add_child(new_attribute)
        
        self._manager.rig.attributes = attributes
        self._manager.ui.create_attributes()

    def refresh_attribute(self, attribute):
        """Get the value of an attribute.

        Args:
            attribute (class: Attribute): The attribute to update
        """
        new_value = cmds.getAttr(f"{attribute.object}.{attribute.name}")

        if(attribute.attribute_type == AttributeTypes.number):
            attribute.value = float(new_value)
        elif(attribute.attribute_type == AttributeTypes.boolean):
            attribute.value = bool(new_value)
        elif(attribute.attribute_type == AttributeTypes.string):
            attribute.value = str(new_value)
        elif(attribute.attribute_type == AttributeTypes.enum):
            attribute.value = int(new_value)

    def refresh_attributes(self, *args):
        """Refresh attributes values.
        """
        if(self._manager.rig == None): return

        for attribute in self._manager.rig.attributes:
            if(attribute.attribute_type == AttributeTypes.group):
                for sub_attribute in attribute.childs:
                    self.refresh_attribute(sub_attribute)
            else:
                self.refresh_attribute(attribute)

        self._manager.ui.refresh_attributes()

    def update_attribute(self, attribute):
        """Update attribute for object.

        Args:
            attribute (class: Attribute): Attribute
        """
        try:
            cmds.setAttr(f"{attribute.object}.{attribute.name}", attribute.value)
        except Exception as e:
            logger.error(f"Failed to set {attribute.object}.{attribute.name} to {attribute.value}")