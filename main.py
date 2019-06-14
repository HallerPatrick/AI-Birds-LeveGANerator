from copy import deepcopy


def main():
    # generate levels using input parameters

    backup_probability_table_blocks = deepcopy(probability_table_blocks)
    backup_materials = deepcopy(materials)

    FILE = open("parameters.txt", 'r')
    checker = FILE.readline()
    finished_levels = 0
    while (checker != ""):
        if checker == "\n":
            checker = FILE.readline()
        else:
            number_levels = int(deepcopy(checker))              # the number of levels to generate
            restricted_combinations = FILE.readline().split(',')      # block type and material combination that are banned from the level
            for i in range(len(restricted_combinations)):
                restricted_combinations[i] = restricted_combinations[i].split()     # if all materials are baned for a block type then do not use that block type
            pig_range = FILE.readline().split(',')
            time_limit = int(FILE.readline())                   # time limit to create the levels, shouldn't be an issue for most generators (approximately an hour for 10 levels)
            checker = FILE.readline()

            restricted_blocks = []                              # block types that cannot be used with any materials
            for key,value in block_names.items():
                completely_restricted = True
                for material in materials:
                    if [material,value] not in restricted_combinations:
                        completely_restricted = False
                if completely_restricted == True:
                    restricted_blocks.append(value)

            probability_table_blocks = deepcopy(backup_probability_table_blocks)
            trihole_allowed = True
            tri_allowed = True
            cir_allowed = True
            cirsmall_allowed = True
            TNT_allowed = True

            probability_table_blocks = remove_blocks(restricted_blocks)     # remove restricted block types from the structure generation process
            if "TriangleHole" in restricted_blocks:
                trihole_allowed = False
            if "Triangle" in restricted_blocks:
                tri_allowed = False
            if "Circle" in restricted_blocks:
                cir_allowed = False
            if "CircleSmall" in restricted_blocks:
                cirsmall_allowed = False

            for current_level in range(number_levels):

                number_ground_structures = randint(2,4)                     # number of ground structures
                number_platforms = randint(1,3)                             # number of platforms (reduced automatically if not enough space)
                number_pigs = randint(int(pig_range[0]),int(pig_range[1]))  # number of pigs (if set too large then can cause program to infinitely loop)

                if (current_level+finished_levels+4) < 10:
                    level_name = "0"+str(current_level+finished_levels+4)
                else:
                    level_name = str(current_level+finished_levels+4)
                
                number_ground_structures, complete_locations, final_pig_positions = create_ground_structures()
                number_platforms, final_platforms, platform_centers = create_platforms(number_platforms,complete_locations,final_pig_positions)
                complete_locations, final_pig_positions = create_platform_structures(final_platforms, platform_centers, complete_locations, final_pig_positions)
                final_pig_positions, removed_pigs = remove_unnecessary_pigs(number_pigs)
                final_pig_positions = add_necessary_pigs(number_pigs)
                final_TNT_positions = add_TNT(removed_pigs)
                number_birds = choose_number_birds(final_pig_positions,number_ground_structures,number_platforms)
                possible_trihole_positions, possible_tri_positions, possible_cir_positions, possible_cirsmall_positions = find_additional_block_positions(complete_locations)
                selected_other = add_additional_blocks(possible_trihole_positions, possible_tri_positions, possible_cir_positions, possible_cirsmall_positions)
                write_level_xml(complete_locations, selected_other, final_pig_positions, final_TNT_positions, final_platforms, number_birds, level_name, restricted_combinations)
            finished_levels = finished_levels + number_levels



if __name__ == "__main__":
    main()