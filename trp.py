
import copy


class Request:
    def __init__(self, id, nodeFrom, nodeTo, profit) -> None:
        self.id = id
        self.nodeFrom = nodeFrom
        self.nodeTo = nodeTo
        self.profit = profit

    
class Vehicle:
    def __init__(self, id, node) -> None:
        self.id = id
        self.node = node

class TRP:
    def __init__(self, nodes_count, dist):
        self.nodes_count = nodes_count
        self.dist = dist

        self.vehicles = []
        self.requests = []

        self.routes = []


    def total_dist(self):
        total_dist = 0.0
        for route in self.routes:
            for i in range(len(route)-1):
                u = route[i]
                v = route[i+1]
                total_dist += self.dist(u,v)

        return total_dist

    def vehicle(self, id) -> Vehicle:
        for v in self.vehicles:
            if v.id == id: return v
        raise KeyError(id)

    def request(self, id) -> Request:
        for r in self.request:
            if r.id == id: return r
        raise KeyError(id)

    def nodes(self):
        nodes = []
        for vehicle in self.vehicles:
            nodes.append(vehicle.node)

        for request in self.requests:
            nodes.append(request.nodeFrom)
            nodes.append(request.nodeTo)

        return nodes

    def edges(self):
        nodes = self.nodes()
        edges = []
        for node1 in nodes:
            for node2 in nodes:
                if node1 == node2: continue
                edges.append((node1, node2))


    def copy(self):
        return copy.deepcopy(self)