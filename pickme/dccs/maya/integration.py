'''
    :package:   PickMe
    :file:      integration.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Maya integration class.
'''
from maya import cmds
from maya.api import OpenMaya

from pickme.core.attribute import AttributeGroup, AttributeTypes, Attribute
from pickme.core.integration import Integration

class MayaIntegration(Integration):
    def __init__(self, manager=None) -> None:
        super(MayaIntegration, self).__init__()
        self._name = "Maya"
        self._manager = manager

        # Adding callbacks
        OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterCreateReference, self._manager.ui.reload_configurations)
        OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterRemoveReference, self._manager.ui.reload_configurations)

        OpenMaya.MEventMessage.addEventCallback("SelectionChanged", self.get_attributes_for_selection)
        OpenMaya.MEventMessage.addEventCallback("timeChanged", self.refresh_attributes)
    
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
    
    def get_attributes_for_selection(self, *args, **kwargs):
        """Get the attributes from the selection.
        """
        attributes = []

        attributes_to_skip = (
            "visibility",
            "translateX",
            "translateY",
            "translateZ",
            "rotateX",
            "rotateY",
            "rotateZ",
            "scaleX",
            "scaleY",
            "scaleZ"
        )

        for sel in cmds.ls(sl=True):
            attributes.append(
                AttributeGroup(
                    self._manager.rig,
                    sel,
                    f"{sel}"
                )
            )

            for attr in cmds.listAttr(sel, keyable=True):
                if(attr in attributes_to_skip): continue
                
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

                attributes[-1].childs.append(new_attribute)
        
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
            print(f"Failed to set {attribute.object}.{attribute.name} to {attribute.value}")