import math
import os
import random

import numpy as np
import simpy
import yaml

from .BaseStation import BaseStation
from .Client import Client
from .Coverage import Coverage
from .Distributor import Distributor
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


def get_random_mobility_pattern(vals, mobility_patterns):
    i = 0
    r = random.random()

    while vals[i] < r:
        i += 1
    
    return mobility_patterns[i]


def get_random_slice_index(vals):
    i = 0
    r = random.random()

    while vals[i] < r:
        i += 1
    return i


def run(env):
    pass


# Read YAML file
CONF_FILENAME = os.path.join(os.path.dirname(__file__), 'example-input.yml')
with open(CONF_FILENAME, 'r') as stream:
    data = yaml.load(stream, Loader=yaml.FullLoader)

random.seed()
env = simpy.Environment()

SLICES_INFO = data['slices']
NUM_CLIENTS = data['num_clients'] # 3
NUM_BASE_STATIONS = data['num_base_stations'] # 3
MOBILITY_PATTERNS = data['mobility_patterns']
BASE_STATIONS = data['base_stations']
CLIENTS = data['clients']



collected, slice_weights = 0, []
for __, s in SLICES_INFO.items():
    collected += s['weight']
    slice_weights.append(collected)

collected, mb_weights = 0, []
for __, mb in MOBILITY_PATTERNS.items():
    collected += mb['weight']
    mb_weights.append(collected)

mobility_patterns = []
for name, mb in MOBILITY_PATTERNS.items():
    mobility_pattern = Distributor(name, get_dist(mb['distribution']), *mb['params'])
    mobility_patterns.append(mobility_pattern)


base_stations = []
i = 0
for b in BASE_STATIONS:
    slices = []
    ratios = b['ratios']
    capacity = b['capacity_bandwidth']
    for name, s in SLICES_INFO.items():
        s_cap = capacity * ratios[name]
        s = Slice(name, ratios[name], None, s['weight'],
                  s['delay_tolerance'],
                  s['qos_class'], s['bandwidth_guaranteed'],
                  s['bandwidth_max'], s_cap)
        s.capacity = simpy.Container(env, init=s_cap, capacity=s_cap)
        slices.append(s)
    b = BaseStation(i, b['x'], b['y'], Coverage((b['x'], b['y']), b['coverage'],), capacity, slices)
    base_stations.append(b)
    i += 1

ufp = CLIENTS['usage_frequency']
usage_freq_pattern = Distributor(f'ufp', get_dist(ufp['distribution']), *ufp['params'])

clients = []
for i in range(NUM_CLIENTS):
    loc_x = CLIENTS['location']['x']
    loc_y = CLIENTS['location']['y']
    location_x = get_dist(loc_x['distribution'])(*loc_x['params'])
    location_y = get_dist(loc_y['distribution'])(*loc_y['params'])
    
    mobility_pattern = get_random_mobility_pattern(mb_weights, mobility_patterns)

    up = CLIENTS['usage']
    usage_pattern = Distributor(f'C_{i}_up', get_dist(up['distribution']), *up['params'])
    connected_slice_index = get_random_slice_index(slice_weights)
    c = Client(env, location_x, location_y,
               mobility_pattern, usage_freq_pattern.generate_scaled(), usage_pattern, connected_slice_index, base_stations[i])
    clients.append(c)

#env.process(client_generator(env, NUM_CLIENTS))
env.run(until=10)
