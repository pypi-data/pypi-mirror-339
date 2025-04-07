import math


def get_squared_distance(position1, position2):
    sqr_delta_x = (position1[0] - position2[0]) ** 2
    sqr_delta_y = (position1[1] - position2[1]) ** 2
    return math.sqrt(sqr_delta_x + sqr_delta_y)


def check_circle_circle_collision(position1, position2, radius1, radius2):
    squared_distance = get_squared_distance(position1, position2)
    return squared_distance < (radius1 + radius2)
