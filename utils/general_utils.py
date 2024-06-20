import math, random

class Object(object):
    pass

# [(0, 0, 0), (1, 0, 0), (2, 3, 0), ...] ==> [(0, 0), (1, 0), (2, 3), ...]
def remove_z_from_tuples(tuple_list: list):
    new_tuple_list = []
    for point in tuple_list:
        new_tuple_list.append((point[0], point[1]))
    return new_tuple_list

# [(0, 0), (1, 0), (2, 3), ...] ==> [(0, 0, 0), (1, 0, 0), (2, 3, 0), ...]
def add_z_to_tuples(tuple_list: list):
    new_tuple_list = []
    for point in tuple_list:
        new_tuple_list.append((point[0], point[1], 0))
    return new_tuple_list

# [0, 0, 1, 0, 2, 3] ==> [(0, 0), (1, 0), (2, 3), ...]
def convert_to_tuples(non_tuple_list: list):
    new_tuple_list = []
    for i in range(0, len(non_tuple_list)-1, 2):
        new_tuple_list.append((non_tuple_list[i], non_tuple_list[i+1]))
    return new_tuple_list

# [(0, 0), (1, 0), (2, 3), ...] ==> [0, 0, 1, 0, 2, 3]
def convert_from_tuples(tuple_list: list):
    non_tuple_list = []
    for tup in tuple_list:
        non_tuple_list += list(tup)
    return non_tuple_list

def in_circle(center_x, center_y, radius, x, y):
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2

def circles_touch(x1, y1, x2, y2, r1, r2):
    d = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    if(d <= r1 - r2) or (d <= r2 - r1) or (d < r1 + r2) or (d == r1 + r2):  return True
    else:                                                                   return False

def generate_point(mean_x, mean_y, deviation_x, deviation_y):
    return random.gauss(mean_x, deviation_x), random.gauss(mean_y, deviation_y)
