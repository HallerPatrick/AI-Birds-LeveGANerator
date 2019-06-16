import xml.etree.ElementTree as ET

class XmlWriter:

    def __init__(self, filename):
        self.filename = filename
        self.root = ET.Element('Level')

    def add_header(self):
        level = ET.SubElement(self.root, "Level")
        level.set("width", "2")
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

    def add_game_objects(self, blocks, pigs, platform):
        game_objects = ET.SubElement(self.root, "GameObjects")

        def add_blocks(blocks):
            pass

        def add_pigs(pigs):
            pass

        def add_platforms(platform):
            pass

        add_blocks(blocks)
        add_pigs(pigs)
        add_platforms(platform)

    def write(self):
        data = ET.tostring(self.root, encoding="utf8", method="xml")
        with open(self.filename, "wb") as f:
            f.write(data)


