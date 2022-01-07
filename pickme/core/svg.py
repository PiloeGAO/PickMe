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
    def __init__(self, id="", parent=None, childs=[]) -> None:
        self.id = id
        self.parent = parent
        self.childs = childs

    def add_child(self, child):
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
                    parent_class.add_child(
                        SVGPath(
                            id=elem.attrib["id"],
                            raw_style=elem.attrib["style"],
                            raw_d=elem.attrib["d"],
                            raw_title=elem["title"] if elem.get("title", None) != None else "",
                            raw_description=elem["desc"] if elem.get("desc", None) != None else ""
                        )
                    )
                else:
                    print("Skipping {elem.tag} (not supported).")

        recursive_import(root, self)

class SVGLayer(SVG):
    def __init__(self, *args, **kwargs) -> None:
        super(SVGLayer, self).__init__(*args, **kwargs)
    
class SVGPath(SVG):
    def __init__(self, raw_style, raw_d, raw_title, raw_description, *args, **kwargs) -> None:
        super(SVGPath, self).__init__(*args, **kwargs)
        self.raw_style = raw_style
        self.raw_d = raw_d
        self.raw_title = raw_title
        self.raw_description = raw_description 

if(__name__ == "__main__"):
    # TODO: Remove this when the implementation is finished.
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    GLOBAL_CONFIG_DIR = os.environ.get("pickme_configs", os.path.join(ROOT_DIR, "configs"))
    
    svg = SVGDocument(path=os.path.join(GLOBAL_CONFIG_DIR, "demo", "picker.svg"))
    print(svg.__dict__)