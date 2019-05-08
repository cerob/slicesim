import math
import os
import random

import numpy as np
import simpy
import yaml

from .BaseStation import BaseStation
from .Client import Client
from .Coverage import Coverage
from .MobilityPattern import MobilityPattern
from .Slice import Slice


def r():
    return random.randint(0, 1000)


def get_dist(d):
    #TODO expand list
    dists = {
        'normal': np.random.normal,
        'randInt': random.randint,
    }
    return dists[d]


def client_generator(env, n):
    for i in range(n):
        yield env.timeout(0)
        env.process(Client(random.randint(0, 1000), random.randint(0, 1000),
                    mobility_pattern, base_stations[i]))


def run(env):
    pass


# Read YAML file
CONF_FILENAME = os.path.join(os.path.dirname(__file__), 'example-input.yml')
with open(CONF_FILENAME, 'r') as stream:
    data = yaml.load(stream, Loader=yaml.FullLoader)

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
        print(ratios)
        s_cap = capacity * ratios[name]
        s = Slice(name, ratios[name], None, s['delay_tolerance'],
                  s['qos_class'], s['bandwidth_guaranteed'],
                  s['bandwidth_max'], s_cap)
        s.capacity = simpy.Container(env, init=s_cap, capacity=s_cap)
        slices.append(s)
    b = BaseStation(b['x'], b['y'], Coverage((b['x'], b['y']), b['coverage'],), capacity, slices)
    base_stations.append(b)

'''clients = []
for i in range(NUM_CLIENTS):
    c = Client(random.randint(0, 1000), random.randint(0, 1000),
                mobility_pattern, base_stations[i])
    clients.append(c)
'''

#env.process(run(env))
#env.run()
