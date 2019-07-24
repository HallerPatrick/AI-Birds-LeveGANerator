import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import xml.etree.ElementTree as ET

class XmlWriter:

    def __init__(self, filename):
        self.xml_file = [
            '<?xml version="1.0" encoding="utf-16"?>',
            '<Level width="2">',
            '<Camera maxWidth="30" minWidth="20" x="0" y="2">'
        ]
        self.filename = filename
        
    def add_birds(self, birds):
        self.xml_file.append('<Birds>')
        for bird in birds:
            self.xml_file.append('<Bird type="{}"/>'.format(bird))
        self.xml_file.append('</Birds>')

    def add_slingshot(self):
        self.xml_file.append('<Slingshot x="-8" y="-2.5">')
        self.xml_file.append('<GameObjects>')

    #### Add objects from class objects
    def add_platform_objects(self, platforms):
        for platform in platforms:
            platform_tag = '<Platform material="" type="Platform" x="{}" y="{}" />'.format(platform.x, platform.y)
            self.xml_file.append(platform_tag)


    def add_pig_objects(self, pigs):
        for pig in pigs:
            pig_tag = '<Pig roation="0" type="{}" material="" x="{}" y="{}" />'.format(pig.type, pig.x, pig.y)
            self.xml_file.append(pig_tag)

    def add_tnt_objects(self, tnts):
        for tnt in tnts:
            tnt_tag = '<TNT material="" rotation="0" type="" x="{}" y="{}" />'.format(tnt.x, tnt.y)
            self.xml_file.append(tnt_tag)

    def add_block_objects(self, blocks):
        for block in blocks:
            block_tag = '<Block material="{}" rotation="0" type="{}" x="{}" y="{}" />'.format(block.material, block.type, block.x, block.y)
            self.xml_file.append(block_tag)

    def write(self):
        self.xml_file.append('</GameObjects>')
        self.xml_file.append('</Level>')

        with open(self.filename, "w") as f:
            f.write("\n".join(self.xml_file))
    
