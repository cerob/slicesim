import math
import os
import sys
import random

import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, MultiPoint
import simpy
import yaml

from .BaseStation import BaseStation
from .Client import Client
from .Coverage import Coverage
from .Distributor import Distributor
from .Graph import Graph
from .Slice import Slice
from .Stats import Stats

from .utils import kdtree_all

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


# Read YAML file
CONF_FILENAME = os.path.join(os.path.dirname(__file__), sys.argv[1])
with open(CONF_FILENAME, 'r') as stream:
    data = yaml.load(stream, Loader=yaml.FullLoader)

random.seed()
env = simpy.Environment()

SETTINGS = data['settings']
SLICES_INFO = data['slices']
NUM_CLIENTS = SETTINGS['num_clients'] # 3
MOBILITY_PATTERNS = data['mobility_patterns']
BASE_STATIONS = data['base_stations']
CLIENTS = data['clients']

if SETTINGS['logging']:
    sys.stdout = open(sys.argv[2],'wt')
else:
    sys.stdout = open(os.devnull, 'w')

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
        # TODO remove bandwidth max
        s = Slice(name, ratios[name], 0, s['weight'],
                  s['delay_tolerance'],
                  s['qos_class'], s['bandwidth_guaranteed'],
                  s['bandwidth_max'], s_cap)
        s.capacity = simpy.Container(env, init=s_cap, capacity=s_cap)
        slices.append(s)
    base_station = BaseStation(i, Coverage((b['x'], b['y']), b['coverage']), capacity, slices)
    base_stations.append(base_station)
    i += 1

ufp = CLIENTS['usage_frequency']
usage_freq_pattern = Distributor(f'ufp', get_dist(ufp['distribution']), *ufp['params'], divide_scale=ufp['divide_scale'])

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
    c = Client(i, env, location_x, location_y,
               mobility_pattern, usage_freq_pattern.generate_scaled(), usage_pattern, connected_slice_index, None)
    clients.append(c)
    # shapely(c)

kdtree_all(clients, base_stations, LIMIT_CLOSEST_POINT=SETTINGS['limit_closest_base_stations'])

stats = Stats(env, base_stations, clients)
env.process(stats.collect())

env.run(until=int(SETTINGS['simulation_time']))

for client in clients:
    print(client)
    print(f'\tTotal connected time: {client.total_connected_time:>5}')
    print(f'\tTotal unconnected time: {client.total_unconnected_time:>5}')
    print(f'\tTotal request count: {client.total_request_count:>5}')
    print(f'\tTotal consume time: {client.total_consume_time:>5}')
    print(f'\tTotal usage: {client.total_usage:>5}')
    print()

print(stats.get_stats())

if SETTINGS['plotting']:
    graph = Graph(base_stations, clients)
    graph.draw_all(*stats.get_stats())
    graph.save_fig()
    graph.show_plot()

sys.stdout = sys.__stdout__
print('Simulation ran successfully and output file created as:',sys.argv[2])