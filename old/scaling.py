def scale_to_size(x, y, scale_x, scale_y):
    if x > 0:
        x_0 = x - \
            (((scale_x / XML_DIM[0]) * ((IMG_DIM[0] / 2) * (IMG_DIM[1] / IMG_DIM[0]))))
        print("XXX")
        print("Add to object space:" + (((scale_x / XML_DIM[0]) * ((IMG_DIM[0] / 2) * (IMG_DIM[1] / IMG_DIM[0])))))
        x_1 = x + \
            (((scale_x / XML_DIM[0]) * ((IMG_DIM[0] / 2) * (IMG_DIM[1] / IMG_DIM[0]))))
        print("Add to object space:" + (((scale_x / XML_DIM[0]) * ((IMG_DIM[0] / 2) * (IMG_DIM[1] / IMG_DIM[0])))))

    if y > 0:
        y_0 = y + ((scale_y / XML_DIM[1]) *
                   ((IMG_DIM[1] / 2) * (IMG_DIM[1] / IMG_DIM[0])))
        print("YYYYY")
        print("addding: " + ((scale_y / XML_DIM[1]) *
                   ((IMG_DIM[1] / 2) * (IMG_DIM[1] / IMG_DIM[0]))))
        print("adding: " + ((scale_y / XML_DIM[1]) *
                   ((IMG_DIM[1] / 2) * (IMG_DIM[1] / IMG_DIM[0]))))
        y_1 = y - ((scale_y / XML_DIM[1]) *
                   ((IMG_DIM[1] / 2) * (IMG_DIM[1] / IMG_DIM[0])))

    return x_0, y_0, x_1, y_1