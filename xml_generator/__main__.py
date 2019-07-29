#!/usr/local/bin/python3

""" This script builds the final xml files used for the angry birds levels. The
steps are written out the the README file"""

import argparse
import os
import shutil
import sys

from random import uniform
from random import randint

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(
    os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


from raw_level_generator.raw_image_builder import convert_coord_back
from raw_level_generator.xml_parser import Platform, Pig, Block, TNT
from baseline import xml_writer
from conture_detector.conture_detector import conture_detector
from nn.img_generator import generate_single_image, generate_25_images
from utils import Parameters


# Amount of image that shall be generated for each game object (4)
IMG_BATCH_SIZE = 30

# Paths to the trained models for all game objects
models = {
    "pig": "../nn/models/pig_generator.h5",
    "block": "../nn/models/block_generator.h5",
    "platform": "../nn/models/platform_generator.h5",
    "tnt": "../nn/models/tnt_generator.h5"
}

# bird types number and probability of being selected
bird_probabilities = {'1': 0.35, '2': 0.2, '3': 0.2, '4': 0.15, '5': 0.1}

# bird types number and name
bird_names = {'1': "BirdRed", '2': "BirdBlue",
              '3': "BirdYellow", '4': "BirdBlack", '5': "BirdWhite"}

# blocks number and probability of being selected
probability_table_blocks = {'1': 0.10, '2': 0.10, '3': 0.10, '4': 0.05,
                            '5': 0.02, '6': 0.05, '7': 0.05, '8': 0.10,
                            '9': 0.05, '10': 0.16, '11': 0.04,
                            '12': 0.16, '13': 0.02}

# blocks number and name
# (blocks 3, 7, 9, 11 and 13) are their respective block names rotated 90 derees clockwise
block_names = {'1': "SquareHole", '2': "RectFat", '3': "RectFat", '4': "SquareSmall",
               '5': "SquareTiny", '6': "RectTiny", '7': "RectTiny", '8': "RectSmall",
               '9': "RectSmall", '10': "RectMedium", '11': "RectMedium",
               '12': "RectBig", '13': "RectBig"}


# Build for every object 25 images
IMG_BATCH_SIZE = 25

GEN_PATH = "gen"
PIG_IMG_PATH = "gen/pig"
BLOCK_IMG_PATH = "gen/block"
TNT_IMG_PATH = "gen/tnt"
PLATFORM_IMG_PATH = "gen/platform"

LEVEL_DIRECTORY = "../game/Science-Birds-Windows/ScienceBirds_Data/StreamingAssets/Levels"


def get_object_centroids():

    generate_25_images(models["pig"], PIG_IMG_PATH)
    generate_25_images(models["block"], BLOCK_IMG_PATH)
    generate_25_images(models["tnt"], TNT_IMG_PATH)
    generate_25_images(models["platform"], PLATFORM_IMG_PATH)


def setup_path():

    if not os.path.exists("gen"):
        os.mkdir("gen")

    if not os.path.exists("gen/pig"):
        os.mkdir("gen/pig")

    if not os.path.exists("gen/block"):
        os.mkdir("gen/block")

    if not os.path.exists("gen/platform"):
        os.mkdir("gen/platform")

    if not os.path.exists("gen/tnt"):
        os.mkdir("gen/tnt")


def get_tnt_centroids():

    print("Generating TNT images")

    counter = 1
    tnt_centroids = []
    while len(tnt_centroids) != 20:
        print("TNT images generated: [%d]\r" % counter, end="")
        print("TNT images used: [%d]\r" % len(tnt_centroids), end="")
        generate_25_images(models["tnt"], TNT_IMG_PATH)
        for image in os.listdir(TNT_IMG_PATH):
            centroids = conture_detector(TNT_IMG_PATH + "/" + image)
            if len(centroids) >= 0 and len(centroids) <= 6:
                # Saving the image as metadata 
                if not os.path.exists("../level/tnt"):
                    os.makedirs("../metadata/tnt")

                shutil.move(TNT_IMG_PATH + "/" + image, "../metadata/tnt/" + image)

                tnt_centroids.append(centroids)

            if len(tnt_centroids) == 20:
                return tnt_centroids

            counter += 1

    return tnt_centroids


def get_platform_centroids():

    print("Generating Platform images")

    counter = 1
    platform_centroids = []
    while len(platform_centroids) != 20:
        print("Platform images generated: [%d]\r" % counter, end="")
        print("Platform images used: [%d]\r" % len(platform_centroids), end="")
        generate_25_images(models["platform"], PLATFORM_IMG_PATH)
        for image in os.listdir(PLATFORM_IMG_PATH):
            centroids = conture_detector(PLATFORM_IMG_PATH + "/" + image)

            # Saving the image as metadata 
            if not os.path.exists("../metadata/platform"):
                os.makedirs("../metadata/platform")
                
            shutil.move(PLATFORM_IMG_PATH + "/" + image, "../metadata/platform/" + image)
            
            platform_centroids.append(centroids)

            if len(platform_centroids) == 20:
                return platform_centroids

            counter += 1

    return platform_centroids


def get_pig_centroids(pig_count):

    pig_min = 4
    pig_max = 8

    print("Generating Pig images")

    counter = 1
    pig_centroids = []
    while len(pig_centroids) != 20:
        print("Pig images generated: [%d]\r" % counter, end="")
        print("Pig images used: [%d]\r" % len(pig_centroids), end="")
        generate_25_images(models["pig"], PIG_IMG_PATH)
        for image in os.listdir(PIG_IMG_PATH):
            centroids = conture_detector(PIG_IMG_PATH + "/" + image)

            if len(centroids) >= pig_min and len(centroids) <= pig_max:

                # Saving the image as metadata 
                if not os.path.exists("../metadata/pig"):
                    os.makedirs("../metadata/pig")
                    
                shutil.move(PIG_IMG_PATH + "/" + image, "../metadata/pig/" + image)

                pig_centroids.append(centroids)

            if len(pig_centroids) == 20:
                return pig_centroids

            counter += 1

    return pig_centroids


def get_block_centroids():

    print("Generating Block images")

    counter = 1
    block_centroids = []
    while len(block_centroids) != 20:
        print("Block images generated: [%d]\r" % counter, end="")
        print("Block images used: [%d]\r" % len(block_centroids), end="")
        generate_25_images(models["pig"], BLOCK_IMG_PATH)
        for image in os.listdir(BLOCK_IMG_PATH):
            centroids = conture_detector(BLOCK_IMG_PATH + "/" + image)

            print(len(block_centroids))
            # Saving the image as metadata 
            if not os.path.exists("../metadata/block"):
                os.makedirs("../metadata/block")
                
            shutil.move(BLOCK_IMG_PATH + "/" + image, "../metadata/block/" + image)
            block_centroids.append(centroids)

            if len(block_centroids) == 20:
                return block_centroids

            counter += 1

    return block_centroids


def build_objects_from_centroids(centroids, game_object):

    objects = []

    for centroid in centroids:
        print("Adding " + game_object + " to level")
        if game_object == Platform.__name__.lower():
            x, y = convert_coord_back(*centroid)
            platform = Platform("Platform", "", str(x), str(y))
            print(platform)
            objects.append(platform)

        if game_object == Pig.__name__.lower():
            x, y = convert_coord_back(*centroid)
            pig = Pig("BasicSmall", "", str(x), str(y), rotation="0")
            print(pig)
            objects.append(pig)

        if game_object == Block.__name__.lower():
            x, y = convert_coord_back(*centroid)
            block_type = block_names[str(choose_item(probability_table_blocks))]
            block = Block(block_type, "wood", str(x), str(y), rotation="0")
            print(block)
            objects.append(block)

        if game_object == TNT.__name__.lower():
            x, y = convert_coord_back(*centroid)
            tnt = TNT("", "", str(x), str(y), rotation="0")
            print(tnt)
            objects.append(tnt)

    return objects

def get_birds():
    birds = []
    for _ in range(randint(3, 7)):
        birds.append(bird_names[str(choose_item(bird_probabilities))])

    return birds

def choose_item(table):
    ran_num = uniform(0.0, 1.0)
    selected_num = 0
    while ran_num > 0:
        selected_num = selected_num + 1
        ran_num = ran_num - table[str(selected_num)]
    return selected_num

def save_level_metadata():
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--parameters_file", required=True,
                        help="Parameters file wiht constraints is passed", default="parameters.txt")
    args = parser.parse_args()

    setup_path()

    print("Reading parameters file")
    parameters = Parameters.parameters_from_file(args.parameters_file)

    tnt_centroids = get_tnt_centroids()
    platform_centroids = get_platform_centroids()
    pig_centroids = get_pig_centroids(parameters[0])
    block_centroids = get_block_centroids()

    for i in range(20):
        writer = xml_writer.XmlWriter("../level/level_{}.xml".format(str(i+4).zfill(2)))
        pig_objects = build_objects_from_centroids(pig_centroids[i], "pig")
        platform_objects = build_objects_from_centroids(
            platform_centroids[i], "platform")
        block_objects = build_objects_from_centroids(block_centroids[i], "block")
        tnt_objects = build_objects_from_centroids(tnt_centroids[i], "tnt")
        birds = get_birds()

        writer.add_birds(birds)
        writer.add_slingshot()
        writer.add_pig_objects(pig_objects)
        writer.add_platform_objects(platform_objects)
        writer.add_block_objects(block_objects)
        writer.add_tnt_objects(tnt_objects)
        writer.write()



    # Clean up
    for level in os.listdir(LEVEL_DIRECTORY):
        os.remove(LEVEL_DIRECTORY + "/" + level)

    # After generating all images copy them into the game level directory
    print("Moving generated levels into game directory")
    for level in os.listdir("../level"):
        shutil.move("../level/" + level, LEVEL_DIRECTORY)


if __name__ == "__main__":
    main()
