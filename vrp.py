

import copy


class Vehicle:
    NONE = None

    def __init__(self, id, capacity, charge):
        self.id = id
        self.capacity = capacity
        self.charge = charge
        self.speed = 0

class Order:
    NONE = None

    def __init__(self, id, node, demand):
        self.id = id
        self.node = node
        self.demand = demand

class Ride:
    def __init__(self, vehicle, nodes):
        self.vehicle = vehicle
        self.nodes = nodes

class VRP:
    def __init__(self, depot_node, nodes_count, dist):
        self.depot_node = depot_node
        self.nodes_count = nodes_count
        self.dist = dist

        self.vehicles = []
        self.orders = []

        self.deliveries = []
        self.rides = []


    def total_dist(self):
        total_dist = 0.0
        for ride in self.rides:
            for i in range(len(ride.nodes)-1):
                u = ride.nodes[i]
                v = ride.nodes[i+1]
                total_dist += self.dist(u,v)

        return total_dist

    def vehicle(self, vehicleId) -> Vehicle:
        for v in self.vehicles:
            if v.id == vehicleId: return v
        raise KeyError(vehicleId)

    def order(self, orderId) -> Order:
        for o in self.orders:
            if o.id == orderId: return o
        raise KeyError(orderId)

    def copy(self):
        return copy.deepcopy(self)