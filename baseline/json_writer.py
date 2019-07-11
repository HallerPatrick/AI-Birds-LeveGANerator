import json

class JsonWriter:

    world = {'camera':[{"bottom": "", "id": "", "left": "", "right": "", "top": "", "x": "", "y": ""}]}

    with open ('sample.json') as json_file:
        data = json.load(json_file)