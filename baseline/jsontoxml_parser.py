import json, xml
from pprint import pprint
from xml_writer import XmlWriter


bird_names = {
    "BIRD_RED": "BirdRed",
    "BIRD_YELLOW": "BirdYellow"
}

gameobjects_names = {
    "WOOD_BLOCK_8X1": "RectFat",
    "WOOD_BLOCK_4X1": "RectSmall",
    "WOOD_BLOCK_2X1": "RectSmall",
    "ICE_BLOCK_4X1": "RectMedium",
    "MISC_ESTRADE_9X3": "CircleSmall",
    "STONE_BLOCK_2X2": "SquareSmall",
    "STONE_BLOCK_2X1": "RectSmall",
    "PIG_BASIC_SMALL": "BasicSmall",
}

material_names = {
    "WOOD_BLOCK_8X1": "wood",
    "WOOD_BLOCK_4X1": "wood",
    "WOOD_BLOCK_2X1": "wood",
    "ICE_BLOCK_4X1": "ice",
    "MISC_ESTRADE_9X3": "",
    "STONE_BLOCK_2X2": "stone",
    "STONE_BLOCK_2X1": "stone",
    "PIG_BASIC_SMALL": "stone",
}


def parse_json(filename):

    with open(filename) as f:
        json_file = json.load(f)

    world = json_file["world"]

    # world holds all blocks and birds
    bird_counts = json_file["counts"]["birds"]
    # block_counts = json_file["counts"]["blocks"]
    # pig_counts = json_file["counts"]["block"]
    # platform_counts = json_file["counts"]["block"]

    # Collect all birds
    birds = []
    # Collect all blocks
    blocks = []
    # Collect all pigs
    pigs = []
    # Collect all platforms
    platforms = []

    # birds
    for key in world.keys():
        if key.startswith("bird"):
            bird_info = world[key]
            birds.append(bird_names[bird_info["id"]])

    assert len(birds) == bird_counts

    # blocks
    for key in world.keys():
        if key.startswith("block"):
            block_type = world[key]
            block_material = world[key]
            blocks.append(gameobjects_names[block_type["id"]])
            blocks.append(material_names[block_material["id"]])
         
    # assert len(blocks) == block_counts

    # pigs
    for key in world.keys():
        if key.startswith("pig"):
            pig_info = world[key]
            pigs.append(gameobjects_names[pig_info["id"]])
    
    # assert len(pigs) == pig_counts

    # platforms
    for key in world.keys():
        if key.startswith("platform"):
            platform_info = world[key]
            platforms.append(gameobjects_names[platform_info["id"]])
        
    # assert len(platforms) == platform_counts

    world_infos = {
        "birds": birds,
        "blocks": blocks,
        "pigs": pigs,
        "platforms": platforms
    }

    construct_xml(world_infos, filename)


def construct_xml(world_infos, filename):
    xml_writer = XmlWriter("baseline/xmls/sample.xml")

    xml_writer.add_header()
    xml_writer.add_birds(world_infos["birds"])
    xml_writer.add_slingshot()
    # TODO: Add gameobjects
    xml_writer.add_blocks(world_infos["blocks"])
    # xml_writer.add_pigs(world_infos["pigs"])
    # xml_writer.add_platforms(world_infos["platforms"])
    xml_writer.write()


def main():
    sample_json = "baseline/sample.json"
    parse_json(sample_json)


if __name__ == "__main__":
    main()
