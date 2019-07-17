import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import xml.etree.ElementTree as ET

class XmlWriter:

    def __init__(self, filename):
        self.filename = filename
        self.root = ET.Element('Level')
        self.root.set("width", "2")
        self.game_objects = ET.SubElement(self.root, "GameObjects")

    def add_header(self):
        camera = ET.SubElement(self.root, "Camera")
        camera.set("x", "0")
        camera.set("y", "2")
        camera.set("minWidth", "20")
        camera.set("maxWidth", "30")

    def add_birds(self, birds):
        birds_eleme = ET.SubElement(self.root, "Birds")
        for bird in birds:
            bird_elem = ET.SubElement(birds_eleme, "Bird")
            bird_elem.set("type", bird)

    def add_slingshot(self):
        slingshot = ET.SubElement(self.root, "Slingshot")
        slingshot.set("x", "-8")
        slingshot.set("y", "-2,5")

    def add_blocks(self, blocks):
        blocks_eleme = ET.SubElement(self.root, "GameObjects")
        for block in blocks:
            blocks_eleme = ET.SubElement(blocks_eleme, "Block")
            blocks_eleme.set("type", block)

    def add_pigs(self, pigs):
        pigs_eleme = ET.SubElement(self.root, "GameObjects")
        for pig in pigs:
            pigs_eleme = ET.SubElement(pigs_eleme, "Pig")
            pigs_eleme.set("type", pig)

    def add_platforms(self, platforms):
        platform_eleme = ET.SubElement(self.root, "GameObjects")
        for platform in platforms:
            platform_eleme = ET.SubElement(platform_eleme, "Platform")
            platform_eleme.set("type", platform)

    def add_game_objects(self):
        self.game_objects = ET.SubElement(self.root, "GameObjects")

    #### Add objects from class objects
    def add_platform_objects(self, platforms):
        for platform in platforms:
            platform_object = ET.SubElement(self.game_objects, "Platform")
            platform_object.set("type", platform.type)
            platform_object.set("x", platform.x)
            platform_object.set("y", platform.y)

    def add_pig_objects(self, pigs):
        for pig in pigs:
            pig_object = ET.SubElement(self.game_objects, "Pig")
            pig_object.set("type", pig.type)
            pig_object.set("x", pig.x)
            pig_object.set("y", pig.y)

    def add_tnt_objects(self, tnts):
        for tnt in tnts:
            tnt_object = ET.SubElement(self.game_objects, "TNT")
            tnt_object.set("type", tnt.type)
            tnt_object.set("x", tnt.x)
            tnt_object.set("y", tnt.y)

    def add_block_objects(self, blocks):
        for block in blocks:
            block_object = ET.SubElement(self.game_objects, "Block")
            block_object.set("type", block.type)
            block_object.set("x", block.x)
            block_object.set("y", block.y)

    
    

    def write(self):
        data = ET.tostring(self.root, encoding="utf8", method="xml")
        with open(self.filename, "wb") as f:
            f.write(data)
