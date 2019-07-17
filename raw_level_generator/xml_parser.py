import xml.etree.ElementTree as ET
from collections import namedtuple
from pprint import pprint
from dataclasses import dataclass

@dataclass
class Block:
    type: str
    material: str
    x: str
    y: str
    rotation: str

@dataclass
class Platform:
    type: str
    material: str
    x: str
    y: str
    rotation: str

@dataclass
class TNT:
    type: str
    material: str
    x: str
    y: str
    rotation: str

@dataclass
class Pig:
    type: str
    material: str
    x: str
    y: str
    rotation: str


def parse_xml(filename):

    root = ET.parse(filename).getroot()
    
    game_objects = {
        "birds": [],
        "block": [],
        "pig": [],
        "platform": [],
        "tnt": []
    }

    for child in root:
        if child.tag == "Birds":
            for bird in child:
                game_objects["birds"].append(bird.attrib["type"])


        if child.tag == "GameObjects":
            for go in child:
                if go.tag == "Block":
                    game_objects["block"].append(
                        Block(
                            go.attrib["type"],
                            go.attrib["material"],
                            go.attrib["x"],
                            go.attrib["y"],
                            go.attrib["rotation"],
                        )
                    )
                if go.tag == "Pig":
                    game_objects["pig"].append(
                        Pig(
                            go.attrib["type"],
                            go.attrib["material"],
                            go.attrib["x"],
                            go.attrib["y"],
                            go.attrib["rotation"],
                        )
                    )
                if go.tag == "Platform":
                    game_objects["platform"].append(
                        Platform(
                            go.attrib["type"],
                            go.attrib["material"],
                            go.attrib["x"],
                            go.attrib["y"],
                        )
                    )
                if go.tag == "TNT":
                    game_objects["tnt"].append(
                        Block(
                            go.attrib["type"],
                            go.attrib["material"],
                            go.attrib["x"],
                            go.attrib["y"],
                            go.attrib["rotation"],
                        )
                    )

    return game_objects


def main():
    parse_xml("gen/level-06.xml")

if __name__ == "__main__":
    main()


