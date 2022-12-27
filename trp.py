
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
    def __init__(self, node, minutes) -> None:
        self.node = node
        self.minutes = minutes

class TRP:
    def __init__(self, dist, minutes = 0):
        self.dist = dist
        self.minutes = 0

        self.vehicles = []
        self.requests = []

        self.routes = []
        self.handled_requests = []


    def tick(self):
        self.minutes += 5

    def update(self):
      
        removed_nodes = []
        i = 0
        while i < len(self.requests):
            req = self.requests[i]
            processable = False
            for vehicle in self.vehicles:
                if (req.twTo - self.travel_time(req.nodeFrom, req.nodeTo) - self.travel_time(vehicle.node, req.nodeFrom)) >= self.minutes:
                    processable = True
                    break

            if not processable:
                removed_nodes.append(req.nodeFrom)
                removed_nodes.append(req.nodeTo)
                self.requests.remove(req)
            else:
                i += 1
        

        for route in self.routes:
            route_vehicle = self.route_vehicle(route)
            for i in range(2, len(route), 2):
                route_point = route[i]
               
                if i == 2 and route_vehicle.node not in removed_nodes:
                    break
                elif i == len(route) - 1:
                    route_vehicle.node = route_point.node
                elif route_point.node not in removed_nodes:
                    route_vehicle.node = route_point.node
                    break
                else:
                    self.handled_requests.append(self.request(route[i-1], route[i]))


        self.routes.clear()

    def travel_time(self, node1, node2):
        dist = self.dist(node1, node2) # Distance in kilometers
        vehicle_speed = 40 # Km/hour
        return (dist/vehicle_speed) * 60

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

    def route_vehicle(self, route) -> Vehicle:
        for v in self.vehicles:
            if v.node == route[0].node: return v
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