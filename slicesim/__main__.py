import math
import os
import random

from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
import numpy as np
import simpy
import yaml

from .BaseStation import BaseStation
from .Client import Client
from .Coverage import Coverage
from .MobilityPattern import MobilityPattern
from .Slice import Slice

from .utils import kdtree, distance

BS_POINTS = []

def r():
    return random.randint(0, 1000)


def get_dist(d):
    #TODO expand list
    dists = {
        'normal': np.random.normal,
        'randInt': random.randint,
    }
    return dists[d]

def shapely(client):

    origin = Point(client.x, client.y)
    nearest_geoms = nearest_points(origin, BS_POINTS)
    near_idx0 = nearest_geoms[0]

    near_idx1 = nearest_geoms[1]


    b = bs_dict.get((near_idx1.x, near_idx1.y))
    d = near_idx0.distance(near_idx1)

    # print("a = ", near_idx0)
    # print(d)
    # print("b = ", near_idx1)

    if d <= b.coverage.radius:
        client.base_station = b


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

mobility_patterns = []
for name, mb in MOBILITY_PATTERNS.items():
    mobility_pattern = MobilityPattern(name, get_dist(mb['distribution']), -10, 10)


base_stations = []
bs_dict = {}
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
    base_station = BaseStation(b['x'], b['y'], Coverage((b['x'], b['y']), b['coverage'],), capacity, slices)
    base_stations.append(base_station)
    bs_dict[(b['x'],b['y'])] = base_station
    BS_POINTS.append(Point(b['x'],b['y']))

BS_POINTS = MultiPoint(BS_POINTS)

clients = []
for i in range(NUM_CLIENTS):
    c = Client(env, random.randint(0, 1000), random.randint(0, 1000),
                mobility_pattern)
    clients.append(c)
    # shapely(c)

kdtree(clients, base_stations)
print(clients[0].base_station)

#env.process(client_generator(env, NUM_CLIENTS))
env.run(until=10)
