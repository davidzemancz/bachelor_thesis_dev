
from itertools import chain, combinations
import math
import random


def powerset(iterable):
    l = list(iterable)
    return chain.from_iterable(combinations(l, r) for r in range(len(l) + 1))

def time_to_str(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  return '{0}:{1}:{2}'.format(int(hours),int(mins),sec)

def rnd_color(f):
  if f == 'hex':
    return "#"+''.join([random.choice('0123456789ABCDEF') for i in range(6)])

def eclidean_norm(cords1, cords2):
    return math.sqrt((cords1[0] - cords2[0])**2 + (cords1[1] - cords2[1])**2)

def manhattan_norm(cords1, cords2):
    return abs(cords1[0] - cords2[0]) + abs(cords1[1] - cords2[1])