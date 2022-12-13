
import copy


class Request:
    def __init__(self, id, nodeFrom, nodeTo, profit, twFrom, twTo) -> None:
        self.id = id
        self.nodeFrom = nodeFrom
        self.nodeTo = nodeTo
        self.profit = profit
        self.twFrom = twFrom
        self.twTo = twTo

class Vehicle:
    def __init__(self, id, node) -> None:
        self.id = id
        self.node = node

class RoutePoint:
    def __init__(self, node, time) -> None:
        self.node = node
        self.time = time

class TRP:
    def __init__(self, dist, time = 0):
        self.dist = dist
        self.time = 0

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
        return None

    def request(self, id) -> Request:
        for r in self.request:
            if r.id == id: return r
        return None

    def nodes(self):
        nodes = []
        for vehicle in self.vehicles:
            nodes.append(vehicle.node)

        for request in self.requests:
            nodes.append(request.nodeFrom)
            nodes.append(request.nodeTo)

        return nodes

    def request(self, nodeFrom, nodeTo):
        for request in self.requests:
            if request.nodeFrom == nodeFrom and request.nodeTo == nodeTo:
                return request
        return None

    def profit(self, nodeFrom, nodeTo):
        req1 = self.request(nodeFrom, nodeTo)
        if req1 is not None: return req1.profit
        else: return 0

    def time_window(self, nodeFrom, nodeTo):
        req1 = self.request(nodeFrom, nodeTo)
        if req1 is not None: return (req1.twFrom, req1.twTo)
        else: return (0,0)

    def edges(self):
        nodes = self.nodes()
        edges = []
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                #if j > i:
                edges.append((node1, node2))
        return edges


    def copy(self):
        return copy.deepcopy(self)