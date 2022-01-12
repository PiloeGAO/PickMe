'''
    :package:   PickMe
    :file:      picker.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     Picker class.
'''
import os

from pickme.core.svg import SVGDocument, SVGLayer, SVGPath

class PickerCore:
    def __init__(self, name, description, interactive_elements=[], manager=None) -> None:
        self._manager = manager
        
        self._name = name
        self._description = description
        self._interactive_elements = interactive_elements
    
    @classmethod
    def create(cls, path, manager=None):
        """Create the Picker Object from a path.

        Args:
            path (str): Path to picker file
            manager (class: Manager, optional): The mPickMe manager. Defaults to None.

        Returns:
            class: Picker: Setuped class
        """
        name = os.path.splitext(path)[0] # TODO: Use the name stored in the SVG.
        description = "" # TODO: Use the description stored in the metadatas of the SVG.
        buttons = []

        print(f"Loading picker: {path}")

        svg_document = SVGDocument(path=path)
        
        for child in svg_document.childs:
            if(type(child) == SVGLayer):
                print("Layers not supported.")
            elif(type(child) == SVGPath):
                buttons.append(
                    PickerInteractiveElement(
                        name=child.id,
                        points=child.svg_draw.points,
                        color=child.svg_style.fill,
                        manager=manager
                    )
                )

        return cls(name, description, buttons, manager=manager)

    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def interactive_elements(self):
        return self._interactive_elements

class PickerInteractiveElement:
    def __init__(self, name="", points=[], color="", manager=None):
        self._manager = manager

        self._name = name
        self._points = points
        self._color = color
    
    @property
    def name(self):
        return self._name
    
    @property
    def points(self):
        return self._points
    
    @property
    def color(self):
        return self._color
    
    def on_click(self):
        """Action to perform on button click.
        """
        self._manager.integration.select_objects(
            [self._name]
        )