from random import uniform
import numpy as np


class BirdRed:
    id = "1"
    prob = 0.35
    
class BirdBlue:
    id = "2"
    prob = 0.2

class BirdYellow:
    id = "3"
    prob = 0.2

class BirdBlack:
    id = "4"
    prob = 0.15

class BirdWhite:
    id = "5"
    prob = 0.1


class Birds:

    
    birds = {
        BirdRed.id : BirdRed,
        BirdBlue.id: BirdBlue,
        BirdYellow.id: BirdYellow,
        BirdBlack.id: BirdBlack,
        BirdWhite.id: BirdWhite
    }

    bird_dist = [
        BirdRed.prob,
        BirdBlue.prob,
        BirdYellow.prob,
        BirdBlack.prob,
        BirdWhite.prob
    ]
    
    def gen_random_birds(self, number_birds):
        ids =  np.random.choice([1, 2, 3, 4, 5], number_birds, p=self.bird_dist)
        return [self.birds[i].__name__ for i in [str(id) for id in ids]]


c = Birds()

print(c.gen_random_birds(4))