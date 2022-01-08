'''
    :package:   PickMe
    :file:      svg.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     SVG parser classes.
'''
import os
import xml.etree.ElementTree as ET

class SVG(object):
    def __init__(self, id="", value="", parent=None, childs=[]) -> None:
        self.id = id
        self.value = value
        self.parent = parent
        self.childs = childs

    def add_child(self, child):
        """Add a child to the SVG class.

        Args:
            child (class): New child to add to list
        """
        child.parent = self
        self.childs.append(child)

class SVGDocument(SVG):
    def __init__(self, path="") -> None:
        super(SVGDocument, self).__init__()
        self.width = 100
        self.height = 100
        self.version = 1.1

        if(os.path.isfile(path)):
            self.load_from_path(path)

    def load_from_path(self, path):
        """Load a SVG from disk and convert it to SVGDocument.

        Args:
            path (str): File path
        """
        tree = ET.parse(path)
        root = tree.getroot()
        
        self.id = root.attrib["id"]
        self.version = root.attrib["version"]

        if("width" in root.attrib.keys()
            and "height" in root.attrib.keys()):
            # Inkscape SVG.
            self.width = root.attrib["width"]
            self.height = root.attrib["height"]
        else:
            # Illustrator SVG.
            viewBox = root.attrib["viewBox"].split(" ")
            self.width = int(viewBox[2])
            self.height = int(viewBox[3])
        
        def recursive_import(parent, parent_class):
            for elem in list(parent):
                if(elem.tag == "{http://www.w3.org/2000/svg}g"):
                    # Create layer
                    new_layer = SVGLayer(
                        id=elem.attrib["id"],
                        childs=[]
                    )
                    parent_class.add_child(
                        new_layer
                    )
                    recursive_import(elem, new_layer)

                elif(elem.tag == "{http://www.w3.org/2000/svg}path"):
                    # Create path
                    new_path = SVGPath(
                        id=elem.attrib["id"],
                        raw_style=elem.attrib["style"],
                        raw_d=elem.attrib["d"]
                    )
                    parent_class.add_child(new_path)
                    recursive_import(elem, new_path)

                elif(elem.tag == "{http://www.w3.org/2000/svg}title" and type(parent_class) == SVGPath):
                    # Create title/desc
                    parent_class.title = SVG(
                        id=elem.attrib["id"],
                        value=elem.text
                    )

                elif(elem.tag == "{http://www.w3.org/2000/svg}desc" and type(parent_class) == SVGPath):
                    # Create title/desc
                    parent_class.description = SVG(
                        id=elem.attrib["id"],
                        value=elem.text
                    )
                else:
                    print(f"Skipping {elem.tag} (not supported).")

        recursive_import(root, self)
    
    def save_to_path(self, path, force_write=False):
        """Save the document to disk.

        Args:
            path (str): Path where the file need to be saved
            force_write (bool, optional): Allow overwrite if file already exist. Defaults to False.

        Raises:
            RuntimeError: File cannot be created
        """
        if(os.path.isfile(path) and force_write):
            os.remove(path)
        elif(os.path.isfile(path) and not force_write):
            raise RuntimeError("File cannot be created.")
        
        root = ET.Element("svg")
        root.attrib["xmlns"] = "http://www.w3.org/2000/svg"
        root.attrib["xmlns:svg"] = "http://www.w3.org/2000/svg"

        def write_attributes_to_elem(svg_obj, elem):
            for tag, value in svg_obj.__dict__.items():
                if(tag in ("childs", "parent")
                    or "raw" in tag):
                    continue
                elem.attrib[tag] = value

        def recursive_creation(svg_obj, elem):
            # TODO: Move the Element creation code to class level.
            write_attributes_to_elem(svg_obj, elem)
            for child in svg_obj.childs:
                if(type(child) == SVGLayer):
                    group_elem = ET.Element("g")
                    elem.append(group_elem)
                    recursive_creation(child, group_elem)
                elif(type(child) == SVGPath):
                    path_elem = ET.Element("path")

                    write_attributes_to_elem(child, path_elem)

                    if(child.title != None):
                        title_elem = ET.Element("title")
                        title_elem.text = child.title.value
                        title_elem.attrib["id"] = child.title.id
                        path_elem.append(title_elem)
                    if(child.description != None):
                        desc_elem = ET.Element("desc")
                        desc_elem.text = child.description.value
                        desc_elem.attrib["id"] = child.description.id
                        path_elem.append(desc_elem)
                    
                    elem.append(path_elem)
                else:
                    print("Unknown child, skipping.")
                    continue
        
        recursive_creation(self, root)
        document = ET.ElementTree()
        document._setroot(root)
        document.write(path, encoding="UTF-8", xml_declaration=True)

class SVGLayer(SVG):
    def __init__(self, *args, **kwargs) -> None:
        super(SVGLayer, self).__init__(*args, **kwargs)
    
class SVGPath(SVG):
    def __init__(self, raw_style, raw_d, title=None, description=None, *args, **kwargs) -> None:
        super(SVGPath, self).__init__(*args, **kwargs)
        self.raw_style = raw_style
        self.raw_d = raw_d
        self.title = title
        self.description = description
    
    @property
    def __dict__(self):
        return {
            "id": self.id,
            "style": self.style,
            "d": self.raw_d
        }

    @property
    def style(self):
        # TODO: Convert the SVGStyle (need to be created) back to xml formating
        return self.raw_style
    
    @property
    def d(self):
        # TODO: Convert SVGPoint (need to be created) back to xml formating
        return self.raw_d

if(__name__ == "__main__"):
    # TODO: Remove this when the implementation is finished.
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    GLOBAL_CONFIG_DIR = os.environ.get("pickme_configs", os.path.join(ROOT_DIR, "configs"))
    
    svg_doc = SVGDocument(path=os.path.join(GLOBAL_CONFIG_DIR, "demo", "picker.svg"))
    print(svg_doc.__dict__)
    svg_doc.save_to_path(os.path.join(GLOBAL_CONFIG_DIR, "demo", "picker_export.svg"), force_write=True)