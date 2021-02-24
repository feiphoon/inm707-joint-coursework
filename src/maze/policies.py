import random
import math

from maze import Step


# Define a random policy
def random_policy(observation):
    return random.choice(list(Step))


def basic_policy(observation):
    coord = observation.dist_to_exit

    # take care about the link between numpy index and directions.

    coord_x = coord[1]
    coord_y = -coord[0]

    angle = math.atan2(coord_y, coord_x)

    if math.pi / 4 <= angle <= 3 * math.pi / 4:
        return Step.UP

    elif -math.pi / 4 <= angle <= math.pi / 4:
        return Step.RIGHT

    elif -3 * math.pi / 4 <= angle <= -math.pi / 4:
        return Step.DOWN

    else:
        return Step.LEFT


def intelligent_policy(observation):
    eps = random.random()
    if eps > 0.8:
        return random_policy(observation)
    else:
        return basic_policy(observation)
