import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import json
import xml
from pprint import pprint
from xml_writer import XmlWriter

from raw_level_generator.xml_parser import Platform, Pig, Block, TNT


bird_names = {
    "BIRD_RED": "BirdRed",
    "BIRD_YELLOW": "BirdYellow",
    "BIRD_BLACK": "BirdBlack",

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

    # Collect all birds
    birds = []
    # Collect all blocks
    blocks = []
    # Collect all pigs
    pigs = []
    # Collect all platforms
    platforms = []

    for key in world.keys():

        # birds
        if key.startswith("bird"):
            bird_info = world[key]
            birds.append(bird_names[bird_info["id"]])

        # blocks
        if key.startswith("block"):

            block_tag = world[key]

            block_id = str(block_tag["id"])

            ### PIGS ###
            if block_id.startswith("PIG"):
                p_type = gameobjects_names[str(block_tag["id"])]
                p_material = material_names[str(block_tag["id"])]
                p_x = str(block_tag["x"])
                p_y = str(block_tag["y"])
                p_rotation = str(block_tag["angle"])
                pig = Pig(p_type, p_material, p_x, p_y, p_rotation)
                pigs.append(pig)

            ###
            elif block_id in gameobjects_names or block_id in material_names:
                b_type = gameobjects_names[str(block_tag["id"])]
                b_material = material_names[str(block_tag["id"])]
                b_x = str(block_tag["x"])
                b_y = str(block_tag["y"])
                b_rotation = ""
                if "rotation" in block_tag:
                    b_rotation = str(block_tag["rotation"])
                block = Block(b_type, b_material, b_x, b_y, b_rotation)
                blocks.append(block)

            else:
                print(block_id)

    world_infos = {
        "birds": birds,
        "blocks": blocks,
        "pigs": pigs
    }

    construct_xml(world_infos, filename)


def construct_xml(world_infos, filename):
    xml_writer = XmlWriter("sample.xml")

    xml_writer.add_header()
    xml_writer.add_slingshot()

    xml_writer.add_birds(world_infos["birds"])

    xml_writer.add_game_objects()
    xml_writer.add_pig_objects(world_infos["pigs"])
    xml_writer.add_block_objects(world_infos["blocks"])

    xml_writer.write()


def main():
    sample_json = "sample.json"
    parse_json(sample_json)


if __name__ == "__main__":
    main()
