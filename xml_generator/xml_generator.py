import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


import json

import xml.etree.ElementTree as ET

from baseline import xml_writer
from raw_level_generator.xml_parser import Platform
from raw_level_generator.raw_image_builder import convert_coord_back
# from conture_detector.conture_detector import 

def read_centroids_from_file(file_name):
    with open(file_name) as f:
        centroid_data = json.load(f)
    return centroid_data


def build_objects_from_centroids(centroids, game_object):

    objects = []

    for centroid in centroids:
        if game_object == Platform.__name__.lower():
            x, y = convert_coord_back(*centroid)
            platform = Platform("Platform", "", str(x), str(y))
            objects.append(platform)

    return objects

def main():

    filename = "centroids.json"

    centroids = read_centroids_from_file(filename)

    platform_objects = build_objects_from_centroids(centroids, "platform")

    writer = xml_writer.XmlWriter(filename)

    writer.add_header()
    writer.add_slingshot()
    writer.add_game_objects()
    writer.add_platform_objects(platform_objects)
    writer.write()


    build_objects_from_centroids(centroids, "platform")

if __name__ == "__main__":
    main()
