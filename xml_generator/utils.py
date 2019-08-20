import os
from copy import deepcopy
from dataclasses import dataclass


block_names = {'1':"SquareHole", '2':"RectFat", '3':"RectFat", '4':"SquareSmall",
               '5':"SquareTiny", '6':"RectTiny", '7':"RectTiny", '8':"RectSmall",
               '9':"RectSmall",'10':"RectMedium",'11':"RectMedium",
               '12':"RectBig",'13':"RectBig"}

# materials that are available
materials = ["wood", "stone", "ice"]



@dataclass
class Parameters:
    """
    This class holds the parameter options of the parameter files that are
    passed to this generator from the competition authorities

    """
    # Amount of levels to generate
    level_count: int
    # Objects that are blacklisted, (material, type)
    object_blacklist: [(str, str)]
    # Range of how many birds to use
    pig_count: (int, int)
    # Time limit for how the generated can maximal take
    time_limit: int

    @classmethod
    def parameters_from_file(cls, filepath):
        """
        :return list of parameter objects
        """

        parameters = []

        file_data = open(filepath, "r")

        checker = file_data.readline()

        while(checker != ""):
            if checker == "\n":
                checker = file_data.readline()
            else:
                number_levels = int(deepcopy(checker))
                restricted_combinations = file_data.readline().split(",")

                blacklist_objects = [(*x.split(), ) for x in restricted_combinations]

                pig_range = file_data.readline().split(",")
                time_limit = int(file_data.readline())

                checker = file_data.readline()

                parameters.append(cls(number_levels, blacklist_objects, pig_range, time_limit))
        
        return parameters

