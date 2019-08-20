#!/usr/local/bin/python3

""" This script builds the final xml files used for the angry birds levels. The
steps are written out the the README file"""

import argparse
import logging

import os
import shutil
import sys

from random import (
    uniform,
    randint,
    randrange
)

# Disable warning infos from tf/keras
logging.getLogger('tensorflow').disabled = True
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(
    os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


from baseline import xml_writer
from xml_generator.utils import Parameters

from conture_detector.conture_detector import conture_detector
from nn.img_generator import generate_single_image, generate_25_images, image_generator
from raw_level_generator.raw_image_builder import convert_coord_back
from raw_level_generator.xml_parser import Platform, Pig, Block, TNT

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

object_to_path = {
   "pig": PIG_IMG_PATH,
   "block": BLOCK_IMG_PATH,
   "tnt": TNT_IMG_PATH,
   "platform": PLATFORM_IMG_PATH 
}

LEVEL_DIRECTORY = "../game/Science-Birds-Windows/ScienceBirds_Data/StreamingAssets/Levels"


def get_object_centroids(game_object, generator_model, level_count, path, is_pig=False):
    """
    Function that generates the amount of centroids given by level_amount

    The images from which the centroids are extracted are saved in a folder and the folder path
    is returned

    :param game_object type of object as string
    :param generator_model, path to saved model and weights
    :param level_count amount of levels that have to be generated, there amount of centroids
    :param path to wich the images should be moved to     
    """

    centroids = []
    
    img_generator = image_generator(generator_model, object_to_path[game_object])

    if not os.path.exists("../metadata/" + game_object):
        os.makedirs("../metadata/" + game_object)




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


def get_tnt_centroids(level_count):

    print("Generating TNT images")

    generator = image_generator(models["tnt"], TNT_IMG_PATH)

    counter = 1
    tnt_centroids = []
    while len(tnt_centroids) != level_count:

        generate_25_images(models["tnt"], TNT_IMG_PATH)

        image_path = next(generator)

        centroids = conture_detector(image_path)

        if len(centroids) >= 0 and len(centroids) <= 6:
            if not os.path.exists("../metadata/tnt"):
                os.makedirs("../metadata/tnt")

            shutil.move(image_path, "../metadata/tnt/" + str(int(image_path.split("/")[-1].replace(".png", "")) + 4) + ".png")

            tnt_centroids.append(centroids)
            counter += 1

        if len(tnt_centroids) == level_count:
            return tnt_centroids

        """
        for image in os.listdir(TNT_IMG_PATH):
            centroids = conture_detector(TNT_IMG_PATH + "/" + image)
            if len(centroids) >= 0 and len(centroids) <= 6:
                # Saving the image as metadata 
                if not os.path.exists("../metadata/tnt"):
                    os.makedirs("../metadata/tnt")

                shutil.move(TNT_IMG_PATH + "/" + image, "../metadata/tnt/" + str(int(image.replace(".png", "")) + 4) + ".png")

                tnt_centroids.append(centroids)

                counter += 1

            if len(tnt_centroids) == level_count:
                return tnt_centroids
        """

    return tnt_centroids


def get_platform_centroids(level_count):

    print("Generating Platform images")

    counter = 1
    platform_centroids = []
    while len(platform_centroids) != level_count:
        print("Platform images generated: [%d]\r" % counter, end="")
        print("Platform images used: [%d]\r" % len(platform_centroids), end="")
        generate_25_images(models["platform"], PLATFORM_IMG_PATH)
        for image in os.listdir(PLATFORM_IMG_PATH):
            centroids = conture_detector(PLATFORM_IMG_PATH + "/" + image)

            # Saving the image as metadata 
            if not os.path.exists("../metadata/platform"):
                os.makedirs("../metadata/platform")
                
            shutil.move(PLATFORM_IMG_PATH + "/" + image, "../metadata/platform/" + str(int(image.replace(".png", "")) + 4) + ".png")
            
            platform_centroids.append(centroids)
            counter += 1

            if len(platform_centroids) == level_count:
                return platform_centroids


    return platform_centroids


def get_pig_centroids(level_count, parameters):

    retry_flag = 5
    retries = 0

    print("Generating Pig images")

    ranges = []
    for parameter in parameters:
        for _ in range(parameter.level_count):
            ranges.append(parameter.pig_count)

    counter = 1
    pig_centroids = []

    reduce_centroids = 1
    while len(pig_centroids) != level_count:

        print("Pig images generated: [%d]\r" % counter, end="")
        print("Pig images used: [%d]\r" % len(pig_centroids), end="")
        generate_25_images(models["pig"], PIG_IMG_PATH)
        for image in os.listdir(PIG_IMG_PATH):
            centroids = conture_detector(PIG_IMG_PATH + "/" + image)
            
            pig_min, pig_max = ranges[counter-1]

            
            if retries % retry_flag == 0:
                for _ in range(len(centroids) - int(pig_max)):
                    centroids.pop(randrange(len(centroids)))
                reduce_centroids += 1

            if len(centroids) >= int(pig_min) and len(centroids) <= int(pig_max):

                # Saving the image as metadata
                if not os.path.exists("../metadata/pig"):
                    os.makedirs("../metadata/pig")
               
                shutil.move(PIG_IMG_PATH + "/" + image, "../metadata/pig/" + str(counter + 3) + ".png")

                pig_centroids.append(centroids)
                counter += 1
            else:
                retries += 1

            if len(pig_centroids) == level_count:
                return pig_centroids


    return pig_centroids


def get_block_centroids(level_count):

    print("Generating Block images")

    counter = 1
    block_centroids = []
    while len(block_centroids) != level_count:
        print("Block images generated: [%d]\r" % counter, end="")
        print("Block images used: [%d]\r" % len(block_centroids), end="")
        generate_25_images(models["pig"], BLOCK_IMG_PATH)
        for image in os.listdir(BLOCK_IMG_PATH):
            centroids = conture_detector(BLOCK_IMG_PATH + "/" + image)

            print(len(block_centroids))
            # Saving the image as metadata 
            if not os.path.exists("../metadata/block"):
                os.makedirs("../metadata/block")
                
            shutil.move(BLOCK_IMG_PATH + "/" + image, "../metadata/block/" + str(int(image.replace(".png", "")) + 4) + ".png")
            block_centroids.append(centroids)

            counter += 1
            if len(block_centroids) == level_count:
                return block_centroids


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--parameters_file", required=True,
                        help="Parameters file wiht constraints is passed", default="parameters.txt")
    args = parser.parse_args()

    setup_path()

    try:
        shutil.rmtree("../metadata")
    except FileNotFoundError:
        pass

    print("Reading parameters file")
    parameters = Parameters.parameters_from_file(args.parameters_file)

    level_count = sum([p.level_count for p in parameters])

    print("Generating {} level...".format(level_count))

    tnt_centroids = get_tnt_centroids(level_count)
    platform_centroids = get_platform_centroids(level_count)
    pig_centroids = get_pig_centroids(level_count, parameters)
    block_centroids = get_block_centroids(level_count)

    i = 0
    for parameter in parameters:
        for _ in range(parameter.level_count):

            #get_object_centroids()

            writer = xml_writer.XmlWriter("../level/level_{}.xml".format(str(i+4)).zfill(2))
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
            i += 1

    # Clean up
    for level in os.listdir(LEVEL_DIRECTORY):
        os.remove(LEVEL_DIRECTORY + "/" + level)


    # After generating all images copy them into the game level directory
    print("Moving generated levels into game directory")
    for level in os.listdir("../level"):
        shutil.move("../level/" + level, LEVEL_DIRECTORY)


if __name__ == "__main__":
    main()
