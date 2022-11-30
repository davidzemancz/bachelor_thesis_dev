import utils
import random
from vrp import VRP
from vrp import VRP,Ride,Vehicle,Order

def generate(orders_count, vehicles_count, seed = None, demands_range = (1,5), capcities_range = (1,20), dist = None) -> VRP:
    
    if dist is None: dist = lambda x, y: utils.eclidean_norm(vrp.cords(x), vrp.cords(y)) 
    vrp = VRP(0, orders_count + 1, dist)

    if seed: random.seed(seed)

    for v_i in range(1, vehicles_count + 1):
        vrp.vehicles.append(Vehicle(v_i, random.randint(capcities_range[0], capcities_range[1]), 1))

    for o_i in range(1, orders_count + 1):
        cords = (random.randint(0, 100), random.randint(0, 100))
        vrp.orders.append(Order(o_i, o_i, random.randint(demands_range[0], demands_range[1]), cords))

    return vrp

