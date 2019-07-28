import unittest
from parameterized import parameterized

import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from raw_level_generator import raw_image_builder as rib

class Test_RawImageBuilder(unittest.TestCase):

    
    @parameterized.expand([
        (64, 10),
        (0, 0),
        (128, 20)
    ])
    def test_map_value_range(self, x, expected):
        actual_x = rib.map_value_range(x, 0, 128, 0, 20)

        self.assertEqual(actual_x, expected)


    @parameterized.expand([
        (-10, -10, (0, 0)),
        (0, 0, (64, 64)),
        (10, -10, (128, 0)),
        (10, 10, (128, 128)),
        (5, 5, (96, 96))
    ])
    def test_convert_coord_(self, x, y, expected):
        self.assertEqual(rib.convert_coord(x, y), expected)


    @parameterized.expand([
        (64, 64, (0, 0)),
        (128, 128, (10, 10)),
        (128, 0, (10, -10)),
        (0, 0, (-10, -10)),
        (96, 96, (5, 5))
    ])
    def test_convert_coord_back(self, x, y, expected):
        self.assertEqual(rib.convert_coord_back(x, y), expected)
    


if __name__ == '__main__':
    unittest.main()