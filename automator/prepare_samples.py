import os
import sys
import time
import shutil

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(
    os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from xml_generator.utils import Parameters

game_levels_dir = "./game/Science-Birds-Windows/ScienceBirds_Data/StreamingAssets/Levels/"

parameters_file = "./parameters.txt"

won_levels_dir = "./raw_level_generator/won_levels/"



def main(level_result_file="./level_result.txt"):

    with open(level_result_file) as f:
        levels = f.readlines()

    for lost_level in levels:
        lost_level = lost_level.strip()
        for level_file in os.listdir(game_levels_dir):
            level = level_file.replace("level_", "").replace(".xml", "")
            if level.startswith("0"):
                level = level[1:]
            if lost_level != level:
                shutil.copyfile(game_levels_dir + level_file, won_levels_dir + str(len(os.listdir(won_levels_dir))) + ".xml")


if __name__ == "__main__":
    main()
