from keras.layers import Dense
from keras.models import Sequential

from xml_parser import parse_xml

##### Input ######

# [ [birds], [block], [pig], [platform],  [tnt] ]

"""
birds
[
    number of birds,
    red 1,
    blue 2,
    yellow 3,
    black 4,
    white 5
]
"""


"""
block
[

]
"""
class LevelGenerator:

    def __init__(self):
        pass

    def build_generator(self):

        content = parse_xml("gen/level-06.xml")


        model = Sequential()

        model.add(Dense(1, activation="relu"))

        model.fit([1], 1)
        model.summary()







        # model.add(Dense())


if __name__ == "__main__":
    lg = LevelGenerator()

    lg.build_generator()