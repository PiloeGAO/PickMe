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
    def __init__(self, id="") -> None:
        self.id = id

class SVGDocument(SVG):
    def __init__(self, path="") -> None:
        super(SVGDocument, self).__init__()
        self.width = 100
        self.height = 100
        self.version = 1.1

        self.layers = []

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
        
        for layer in list(root):
            if(layer.tag != "{http://www.w3.org/2000/svg}g"):
                print(f"Element not supported: {layer.tag}")
                continue
            
            layer_paths = []

            for child in list(layer):
                if(child.tag != "{http://www.w3.org/2000/svg}path"):
                    print(f"Element not supported: {layer.tag}")
                    continue

                layer_paths.append(
                    SVGPath(
                        id=child.attrib["id"],
                        raw_style=child.attrib["style"],
                        raw_d=child.attrib["d"],
                        raw_title=child["title"] if child.get("title", None) != None else "",
                        raw_description=child["desc"] if child.get("desc", None) != None else ""
                    )
                )

            self.layers.append(
                SVGLayer(
                    id=layer.attrib["id"],
                    paths=layer_paths
                )
            )

class SVGLayer(SVG):
    def __init__(self, id="", paths=[]) -> None:
        super(SVGLayer, self).__init__(id=id)
        self.paths = paths

class SVGPath(SVG):
    def __init__(self, id, raw_style, raw_d, raw_title, raw_description) -> None:
        super(SVGPath, self).__init__(id=id)
        self.raw_style = raw_style
        self.raw_d = raw_d
        self.raw_title = raw_title
        self.raw_description = raw_description 

if(__name__ == "__main__"):
    # TODO: Remove this whent the implementation is finished.
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    GLOBAL_CONFIG_DIR = os.environ.get("pickme_configs", os.path.join(ROOT_DIR, "configs"))
    
    svg = SVGDocument(path=os.path.join(GLOBAL_CONFIG_DIR, "demo", "picker.svg"))
    print(svg.__dict__)