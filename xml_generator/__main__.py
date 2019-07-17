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
from nn.img_generator import generate_single_image
from conture_detector.conture_detector import conture_detector

# Amount of image that shall be generated for each game object (4)
IMG_BATCH_SIZE = 30

# Paths to the trained models for all game objects
models = {
    "pig": "nn/models/pig_generator.h5",
    "block": "nn/models/block_generator.h5",
    "platform": "nn/models/platform_generator.h5",
    "tnt": "nn/models/tnt_generator.h5"
}



def get_object_centroids():
    
    for i in range(IMG_BATCH_SIZE):
        # Preload every model
        pig_img_path = generate_single_image(models["pig"], "pig.png")
        block_img_path = generate_single_image(models["block"], "block.png")
        platform_img_path = generate_single_image(models["platform"], "platform.png")
        tnt_img_path = generate_single_image(models["tnt"], "tnt.png")

        print(conture_detector(pig_img_path))




def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--parameters_file", help="Parameters file wiht constraints is passed", default="parameters.txt")
    args = parser.parse_args()



    parameters = Parameters.parameters_from_file(args.parameters_file)

    get_object_centroids()



if __name__ == "__main__":
    main()
