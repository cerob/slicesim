import math
import random
import simpy
import yaml #TODO
import numpy as np


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

def get_dist(d):
    dists = {
        'normal': np.random.normal,
        'randInt': random.randint,
    }
    return dists[d]


def run(env):
    pass


if __name__ == '__main__':

    # Read YAML file
    with open("examples/example-input.yml", 'r') as stream:
        data = yaml.load(stream)

    # print(data)
    random.seed()
    env = simpy.Environment()

    SLICES_INFO = data['slices']
    NUM_CLIENTS = data['num_clients'] # 3
    NUM_BASE_STATIONS = data['num_base_stations'] # 3
    MOBILITY_PATTERNS = data['mobility_patterns']
    BASE_STATIONS = data['base_stations']
    CLIENTS = data['clients']

    mobility_patterns = []
    for name, mb in MOBILITY_PATTERNS.items():
        mobility_pattern = MobilityPattern(name, get_dist(mb['distribution']), -10, 10)

    base_stations = []
    for b in BASE_STATIONS:
        slices = []
        ratios = b['ratios']
        capacity = b['capacity_bandwidth']
        for name, s in SLICES_INFO.items():
            s_cap = capacity * ratios[name]
            s = Slice(name, ratios[name], None, s['delay_tolerance'],
                      s['qos_class'], s['bandwidth_guaranteed'],
                      s['bandwidth_max'], s_cap)
            s.capacity = simpy.Container(env, init=s_cap, capacity=s_cap)
            slices.append(s)
        b = BaseStation(b['x'], b['y'], Coverage((b['x'], b['y']), b['coverage'], capacity, slices)
        base_stations.append(b)

    clients = []
    for i in range(NUM_CLIENTS):
        c = Client(random.randint(0, 1000), random.randint(0, 1000),
                   mobility_pattern, base_stations[i])
        clients.append(c)

    #env.process(run(env))
    #env.run()
