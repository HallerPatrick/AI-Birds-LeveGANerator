import xml.etree.ElementTree as ET

class XmlWriter:

    def __init__(self, filename):
        self.filename = filename
        self.root = ET.Element('Level')
        self.root.set("width", "2")

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

    def add_game_objects(self):
        self.game_objects = ET.SubElement(self.root, "GameObjects")

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

    def write(self):
        data = ET.tostring(self.root, encoding="utf8", method="xml")
        with open(self.filename, "wb") as f:
            f.write(data)


