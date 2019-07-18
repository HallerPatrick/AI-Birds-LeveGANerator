from PIL import Image, ImageDraw
import os
from xml_parser import parse_xml

# FROM: XML (-9.99999, -9.99999), (9.99999, 9.99999)
# TO: PIL X: (0, 0) Y: (Pixel_max_x, Pixel_max_y)

IMG_DIM = (128, 128)
XML_DIM = (10, 10)

PIG_SIZE = 0.5

# Colors

PIG_COLOR = (255, 105, 180, 1)  # pink
BLOCK_COLOR = (0, 255, 0, 1)  # grenn
PLATFORM_COLOR = (255, 255, 255, 1)  # white
TNT_COLOR = (255, 0, 0, 1)

block_names = {
    "SquareHole": "1", "RectFat": '2', "RectFat": '3', "SquareSmall": '4',
    "SquareTiny": '5', "RectTiny": '6', "RectTiny": '7', "RectSmall": '8',
    "RectSmall": '9', "RectMedium": '10', "RectMedium": '11', "RectBig": '12',
    "RectBig": '13'
}

# blocks number and size
blocks = {'1': [0.84, 0.84], '2': [0.85, 0.43], '3': [0.43, 0.85], '4': [0.43, 0.43],
          '5': [0.22, 0.22], '6': [0.43, 0.22], '7': [0.22, 0.43], '8': [0.85, 0.22],
          '9': [0.22, 0.85], '10': [1.68, 0.22], '11': [0.22, 1.68],
          '12': [2.06, 0.22], '13': [0.22, 2.06]}

# Sizes
PIG_SIZE = 0.5
PLATFORM_SIZE = 0.62

# additional objects number and name
additional_objects = {"TriangleHole": "1",
                      "Triangle": "2", "Circle": "3", "CircleSmall": "4"}

# additional objects number and size
additional_object_sizes = {'1': 0.82, '2': 0.82, '3': 0.8, '4': 0.45}


def convert_coord(x, y):
    if x > 0:
        #         MIDDLE POINT X-Axis + relational length * absolute length
        x_value = (IMG_DIM[0] / 2) + (x / XML_DIM[0] * (IMG_DIM[0] / 2))
    else:
        x_value = (IMG_DIM[0] / 2) - ((abs(x) / XML_DIM[0]) * (IMG_DIM[0] / 2))

    if y > 0:
        y_value = (IMG_DIM[1] / 2) + (y / XML_DIM[1] * (IMG_DIM[1] / 2))
    else:
        y_value = (IMG_DIM[1] / 2) - ((abs(y) / XML_DIM[1]) * (IMG_DIM[1] / 2))

    return x_value, y_value

def convert_coord_back(x, y):
    if x > 0:
        #         MIDDLE POINT X-Axis + relational length * absolute length
        x_value = (XML_DIM[0] / 2) + (x / IMG_DIM[0] * (XML_DIM[0] / 2))
    else:
        x_value = (XML_DIM[0] / 2) - ((abs(x) / IMG_DIM[0]) * (XML_DIM[0] / 2))

    if y > 0:
        y_value = (XML_DIM[1] / 2) + (y / IMG_DIM[1] * (XML_DIM[1] / 2))
    else:
        y_value = (XML_DIM[1] / 2) - ((abs(y) / IMG_DIM[1]) * (XML_DIM[1] / 2))

    return x_value, y_value


def scale_to_size(x, y, scale_x, scale_y):
    if x > 0:
        x_0 = x - \
            (((scale_x / XML_DIM[0]) *
              ((IMG_DIM[0] / 2) * (IMG_DIM[1] / IMG_DIM[0]))))
        x_1 = x + \
            (((scale_x / XML_DIM[0]) *
              ((IMG_DIM[0] / 2) * (IMG_DIM[1] / IMG_DIM[0]))))

    if y > 0:
        y_0 = y - ((scale_y / XML_DIM[1]) *
                   ((IMG_DIM[1] / 2) * (IMG_DIM[1] / IMG_DIM[0])))
        y_1 = y + ((scale_y / XML_DIM[1]) *
                   ((IMG_DIM[1] / 2) * (IMG_DIM[1] / IMG_DIM[0])))

    return x_0, y_0, x_1, y_1


def build_block_image(data, path):

    img = Image.new('RGB', IMG_DIM)
    d = ImageDraw.Draw(img)

    for block in data["block"]:
        if block.type in block_names:
            sizex = blocks[block_names[block.type]][0]
            sizey = blocks[block_names[block.type]][1]
        else:
            sizex = additional_object_sizes[additional_objects[block.type]]
            sizey = additional_object_sizes[additional_objects[block.type]]

        co1 = convert_coord(float(block.x) + (sizex * 0.3),
                            float(block.y) + (sizex * 0.3))
        co2 = convert_coord(float(block.x) - (sizey * 0.3),
                            float(block.y) - (sizey * 0.3))

        d.rectangle([co1, co2], fill=PLATFORM_COLOR)

    img.save("out/block/" + path + ".png")


def build_pig_image(data, path):

    img = Image.new('RGB', IMG_DIM)
    d = ImageDraw.Draw(img)

    for pig in data["pig"]:
        co1 = convert_coord(float(pig.x) + 0.5, float(pig.y) + 0.5)
        co2 = convert_coord(float(pig.x) - 0.5, float(pig.y) - 0.5)
        # co2 = scale_to_size(co[0], co[1], PIG_SIZE, PIG_SIZE)
        d.rectangle([co1, co2], fill=PLATFORM_COLOR)

    img.save("out/pig/" + path + ".png")


def build_tnt_image(data, path):

    img = Image.new('RGB', IMG_DIM)
    d = ImageDraw.Draw(img)

    for tnt in data["tnt"]:
        co1 = convert_coord(float(tnt.x) + (PIG_SIZE * 0.3),
                            float(tnt.y) + (PIG_SIZE * 0.3))
        co2 = convert_coord(float(tnt.x) - (PIG_SIZE * 0.3),
                            float(tnt.y) - (PIG_SIZE * 0.3))
        d.rectangle([co1, co2], fill=PLATFORM_COLOR)

    img.save("out/tnt/" + path + ".png")


def build_platform_image(data, path):
    img = Image.new('RGB', IMG_DIM)
    d = ImageDraw.Draw(img)
    for platform in data["platform"]:
        co1 = convert_coord(float(
            platform.x) + (PLATFORM_SIZE * 0.3), float(platform.y) + (PLATFORM_SIZE * 0.3))
        co2 = convert_coord(float(
            platform.x) - (PLATFORM_SIZE * 0.3), float(platform.y) - (PLATFORM_SIZE * 0.3))
        d.rectangle([co1, co2], fill=PLATFORM_COLOR)

    img.save("out/platform/" + path + ".png")


def main():

    sample_folder = "../baseline/samples/"

    if not os.path.exists("out"):
        os.makedirs("out")

    if not os.path.exists("out/pig"):
        os.makedirs("out/pig")

    if not os.path.exists("out/platform"):
        os.makedirs("out/platform")

    if not os.path.exists("out/tnt"):
        os.makedirs("out/tnt")

    if not os.path.exists("out/block"):
        os.makedirs("out/block")

    for path in os.listdir(sample_folder):
        data = parse_xml(sample_folder + path)

        # Build four different images
        build_pig_image(data, path)
        build_block_image(data, path)
        build_platform_image(data, path)
        build_tnt_image(data, path)


if __name__ == '__main__':
    main()
