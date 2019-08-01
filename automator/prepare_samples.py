import os
import sys
import time

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(
    os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from xml_generator.utils import Parameters



def main():

    level_result_file = sys.argv[1]
    parameters_file = "./parameters.txt"
    parameters = Parameters.parameters_from_file(parameters_file)

    level_count = sum([p.level_count for p in parameters])

    found_levels = 0

    while found_levels != level_count:
        
        with open(level_result_file, "r") as f:
            lines = f.readlines()

        found_levels = len(lines)

        print(found_levels)

        time.sleep(5)


if __name__ == "__main__":
    main()
