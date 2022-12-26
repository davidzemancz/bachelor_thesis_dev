import utils
import random
from trp import TRP,Vehicle,Request

GRID_SIZE = 30 # 30x30 km

def generate(requests_count, vehicles_count, seed = None, dist = None) -> TRP:
    
    if dist is None: dist = lambda x, y: utils.manhattan_norm(x, y) 
    trp = TRP(dist, 0)

    if seed: random.seed(seed)

    for v_i in range(1, vehicles_count + 1):
        node = rnd_pos()
        trp.vehicles.append(Vehicle(v_i, node))

    for _ in range(1, requests_count + 1):
      trp.requests.append(get_request(trp))

    return trp


def next_request(trp : TRP) -> TRP:
    trp.requests.append(get_request(trp))
    return trp

def get_request(trp) -> Request:
    nodeFrom = rnd_pos()
    nodeTo = rnd_pos()
    profit = 5 * trp.dist(nodeFrom, nodeTo)
    twFrom = trp.minutes + random.randint(5, 30)
    twTo = twFrom + trp.travel_time(nodeFrom, nodeTo) + random.randint(5, 30)
    return Request(len(trp.requests) + 1, nodeFrom, nodeTo, profit, twFrom, twTo)
    

def rnd_pos():
    return (random.uniform(0, GRID_SIZE), random.uniform(0, GRID_SIZE))