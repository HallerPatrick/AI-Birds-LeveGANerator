#!/usr/local/bin/python3

""" This script builds the final xml files used for the angry birds levels. The
steps are written out the the README file"""

import argparse
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from utils import Parameters
from nn.img_generator import generate_single_image, generate_25_images
from conture_detector.conture_detector import conture_detector

# Amount of image that shall be generated for each game object (4)
IMG_BATCH_SIZE = 30

# Paths to the trained models for all game objects
models = {
    "pig": "../nn/models/pig_generator.h5",
    "block": "../nn/models/block_generator.h5",
    "platform": "../nn/models/platform_generator.h5",
    "tnt": "../nn/models/tnt_generator.h5"
}

# Build for every object 25 images
IMG_BATCH_SIZE = 25

GEN_PATH = "gen"
PIG_IMG_PATH = "gen/pig"
BLOCK_IMG_PATH = "gen/block"
TNT_IMG_PATH = "gen/tnt"
PLATFORM_IMG_PATH = "gen/platform"

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
    

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--parameters_file", required=True, help="Parameters file wiht constraints is passed", default="parameters.txt")
    args = parser.parse_args()

    setup_path()

    parameters = Parameters.parameters_from_file(args.parameters_file)

    get_object_centroids()



if __name__ == "__main__":
    main()
