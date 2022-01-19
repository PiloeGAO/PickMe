'''
    :package:   PickMe
    :file:      picker.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     Picker class.
'''
import os

from pickme.core.exceptions import CoreError
from pickme.core.svg import SVG, SVGDocument, SVGLayer, SVGPath, SVGPoint

from pickme.core.logger import get_logger
logger = get_logger()

class PickerCore:
    def __init__(self, name, description, interactive_elements=[], size=(0, 0), manager=None, svg_document=None) -> None:
        self._manager = manager

        self._svg_document = svg_document
        
        self._name = name
        self._description = description
        self._interactive_elements = interactive_elements
        self._size = size
    
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def interactive_elements(self):
        return self._interactive_elements

    @interactive_elements.setter
    def interactive_elements(self, items):
        self._interactive_elements = items
    
    @property
    def width(self):
        return self._size[0]
    
    @property
    def height(self):
        return self._size[1]
    
    @classmethod
    def create(cls, path, manager=None):
        """Create the Picker Object from a path.

        Args:
            path (str): Path to picker file
            manager (class: Manager, optional): The mPickMe manager. Defaults to None.

        Returns:
            class: Picker: Setuped class
        """
        logger.info(f"Loading picker: {path}")

        name = os.path.splitext(os.path.basename(path))[0]
        description = "" # TODO: Use the description stored in the metadatas of the SVG.
        svg_document = SVGDocument.create(path)
        document_size = (float(svg_document.width), float(svg_document.height))

        picker_core_class = cls(
            name,
            description,
            [],
            size=document_size,
            manager=manager,
            svg_document=svg_document
        )
        
        interactive_elements = []
        for child in svg_document.childs:
            if(type(child) == SVGLayer):
                logger.warning("Layers not supported.")
            elif(type(child) == SVGPath):
                nice_name = child.title.value if child.title != None else child.id

                interactive_elements.append(
                    PickerInteractiveElement(
                        name=child.id,
                        nice_name=nice_name,
                        points=child.svg_draw.points,
                        color=child.svg_style.fill,
                        parent=picker_core_class
                    )
                )

        picker_core_class.interactive_elements = interactive_elements
        return picker_core_class
    
    def save(self):
        """Save the picker to disk.
        """
        self._svg_document.childs = []

        for interactive_element in self._interactive_elements:
            svg_title = SVG(
                id=f"{interactive_element.nice_name.replace(' ', '_')}_title",
                value=interactive_element.nice_name
            )

            new_path = SVGPath(
                "",
                "",
                id=interactive_element.name,
                title=svg_title
            )

            new_path.svg_style.fill = interactive_element.color
            new_path.svg_draw.points = interactive_element.points

            self._svg_document.add_child(
                new_path
            )
        
        self._svg_document.save(force_write=True)
    
    def add_interactive_element(self, name="", nice_name="", color="#FFFFFF", points=[]):
        """Create a new interactive element.

        Args:
            name (str, optional): Name of the object to select. Defaults to "".
            nice_name (str, optional): Name to display. Defaults to "".
            points (list, optional): Position of points that containt the polygon. Defaults to [].
        """
        if(len(points) < 3):
            raise CoreError("Interactive element need valid points positions (3+)")

        svg_points = []
        for pos in points:
            svg_points.append(
                SVGPoint(
                    pos[0],
                    pos[1]
                )
            )
        
        self._interactive_elements.append(
            PickerInteractiveElement(
                name=name,
                nice_name=nice_name,
                points=svg_points,
                color=color,
                parent=self
            )
        )

        self.save()
    
    def remove_interactive_element(self, interactive_element):
        """Remove interactive element from the picker.

        Args:
            interactive_element (class: PickerInteractiveElement): The element to remove
        """
        self._interactive_elements = [elem for elem in self._interactive_elements if elem != interactive_element]
        self.save()

class PickerInteractiveElement:
    def __init__(self, name="", nice_name="", points=[], color="", parent=None):
        self._parent = parent
        self._manager = self._parent._manager

        self._name = name
        self._nice_name = nice_name
        self._points = points
        self._color = color
    
    @property
    def name(self):
        return self._name
    
    @property
    def nice_name(self):
        return self._nice_name
    
    @nice_name.setter
    def nice_name(self, new_name):
        self._nice_name = new_name

    @property
    def points(self):
        return self._points
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, new_color):
        self._color = new_color
    
    def on_click(self):
        """Action to perform on button click.
        """
        self._manager.integration.select_objects(
            [self._name]
        )