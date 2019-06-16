from PIL import Image, ImageDraw
import os
from xml_parser import parse_xml


# FROM: XML (-9.99999, -9.99999), (9.99999, 9.99999)
# TO: PIL X: (0, 0) Y: (Pixel_max_x, Pixel_max_y)

IMG_DIM = (512, 256)
XML_DIM = (10, 10)

PIG_SIZE = 0.5



def convert_coord(x, y):
    if x > 0:
        #         MIDDLE POINT X-Axis + relational length * absolute length
        x_value = (IMG_DIM[0] / 2) +  (x / XML_DIM[0] * (IMG_DIM[0] / 2))
    else:
        x_value = (IMG_DIM[0] / 2) - ((abs(x) / XML_DIM[0]) * (IMG_DIM[0] / 2))
    
    
    if y > 0:
        y_value = (IMG_DIM[1] / 2) + (y / XML_DIM[1] * (IMG_DIM[1] / 2))
    else:
        y_value = (IMG_DIM[1] / 2) - ((abs(y) / XML_DIM[1]) * (IMG_DIM[1] / 2))

    return x_value, y_value
    
def scale_to_size(x, y, scale_x, scale_y):
    if x > 0:
        x_0 = x - (((scale_x / XML_DIM[0]) * ((IMG_DIM[0] / 2)  * (IMG_DIM[1] / IMG_DIM[0])  ))) 
        x_1 = x + (((scale_x / XML_DIM[0]) * ((IMG_DIM[0] / 2)  * (IMG_DIM[1] / IMG_DIM[0])  )))
    
    if y > 0:
        y_0 = y - ((scale_y / XML_DIM[1]) * ((IMG_DIM[1] / 2)  * (IMG_DIM[1] / IMG_DIM[0]) ))
        y_1 = y + ((scale_y / XML_DIM[1]) * ((IMG_DIM[1] / 2)  * (IMG_DIM[1] / IMG_DIM[0]) ))

    return x_0, y_0, x_1, y_1



def main():

    for path in os.listdir("gen"):
        print(path)
        data = parse_xml("gen/" + path)

        img = Image.new('RGB', (512, 256))
        d = ImageDraw.Draw(img)

        for block in data["block"]:
            co = convert_coord(float(block.x), float(block.y))
            d.point([co])
        
        for pig in data["pig"]:
            co1 = convert_coord(float(pig.x) + 0.5, float(pig.y) + 0.5)
            co2 = convert_coord(float(pig.x) - 0.5, float(pig.y) - 0.5)
            # co2 = scale_to_size(co[0], co[1], PIG_SIZE, PIG_SIZE)
            d.rectangle([co1, co2], fill=(255,105,180, 1))


        img.save("out/" +  path + ".png")



if __name__ == '__main__':
    main()
    


