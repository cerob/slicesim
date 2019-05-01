import math
import random
import simpy
import yaml #TODO


class Coverage:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    
    def _get_gaussian_distance(self, p):
        return math.sqrt(sum((i-j)**2 for i,j in zip(p, self.center)))

    def is_in_coverage(self, x, y):
        return _get_gaussian_distance((x,y)) <= self.radius

class BaseStation:
    def __init__(self, x, y, coverage, capacity_bandwidth, slices=None):
        self.x = x
        self.y = y
        self.coverage = coverage
        self.capacity_bandwidth = capacity_bandwidth
        self.slices = slices

class MobilityPattern:
    def __init__(self, name, distribution, *dist_params):
        self.name = name
        self.distribution = distribution
        self.dist_params = dist_params
    
    def generate_movement(self):
        x = self.distribution(*self.dist_params)
        y = self.distribution(*self.dist_params)
        return x, y

class Client:
    def __init__(self, x, y, mobility_pattern, base_station=None):
        self.x = x
        self.y = y
        self.mobility_pattern = mobility_pattern
        self.base_station = base_station
    
    def connect_to_closest_base_station():
        self.base_station = None #TODO

class Slice:
    #TODO make some vars static
    def __init__(self, name, ratio,
                 connected_users, delay_tolerance, qos_class,
                 bandwidth_guaranteed, bandwidth_max, init_capacity):
        self.name = name
        self.connected_users = connected_users
        self.delay_tolerance = delay_tolerance
        self.qos_class = qos_class
        self.ratio = ratio
        self.bandwidth_guaranteed = bandwidth_guaranteed
        self.bandwidth_max = bandwidth_max
        self.init_capacity = init_capacity
        self.capacity = 0

def r():
    return random.randint(0, 1000)


def run(env):
    pass


if __name__ == '__main__':
    random.seed()
    env = simpy.Environment()

    SLICES_INFO = {
        'iot': {
            'delay_tolerance': 10,
            'qos_class': 2,
            'bandwidth_guaranteed': 10,
            'bandwidth_max': 1000,
        },
        'data': {
            'delay_tolerance': 2000,
            'qos_class': 4,
            'bandwidth_guaranteed': 1000,
            'bandwidth_max': 50000,
        },
    }
    NUM_CLIENTS = 3
    NUM_BASE_STATIONS = 3

    mobility_pattern = MobilityPattern('mb', random.randint, -10, 10)

    base_stations = []
    for i in range(NUM_BASE_STATIONS):
        slices = []
        j, ratios = 0, [0.4, 0.6]
        capacity = 1000
        for name, s in SLICES_INFO.items():
            s_cap = capacity * ratios[j]
            s = Slice(name, ratios[j], None, s['delay_tolerance'],
                      s['qos_class'], s['bandwidth_guaranteed'],
                      s['bandwidth_max'], s_cap)
            s.capacity = simpy.Container(env, init=s_cap, capacity=s_cap)
            slices.append(s)
            j += 1
        b = BaseStation(r(), r(), Coverage(r(), r()), capacity, slices)
        base_stations.append(b)

    clients = []
    for i in range(NUM_CLIENTS):
        c = Client(random.randint(0, 1000), random.randint(0, 1000),
                   mobility_pattern, base_stations[i])
        clients.append(c)

    #env.process(run(env))
    #env.run()
