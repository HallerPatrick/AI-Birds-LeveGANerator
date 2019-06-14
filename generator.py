from xml_writer import XmlWriter
from models import Birds


def write_xml(current_level, number_birds, blocks, pigs, platform):

    xml_writer = XmlWriter("level-{}".format(current_level))
    xml_writer.add_header()

    # For now generate birds random
    xml_writer.add_birds(Birds.gen_random_birds(number_birds))

    xml_writer.add_slingshot()

    xml_writer.add_game_objects(
        blocks=blocks,
        pigs=pigs,
        platform=platform
    )

    xml_writer.write()

