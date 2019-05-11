import math
import time

import operator
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
from sklearn.neighbors import KDTree


def distance(a, b):
    return math.sqrt(sum((i-j)**2 for i,j in zip(a, b)))

# Initial connections using k-d tree
def kdtree(clients, base_stations):

    c_coor = [(c.x,c.y) for c in clients]
    bs_coor = [p.coverage.center for p in base_stations]

    tree = KDTree(bs_coor, leaf_size=2)
    res = tree.query(c_coor)

    for c, d, p in zip(clients, res[0], res[1]):
        if d[0] <= base_stations[p[0]].coverage.radius:
            c.base_station = base_stations[p[0]]

# Initial connections using k-d tree
def kdtree_all(clients, base_stations, LIMIT_CLOSEST_POINT=1):

    c_coor = [(c.x,c.y) for c in clients]
    bs_coor = [p.coverage.center for p in base_stations]

    tree = KDTree(bs_coor, leaf_size=2)
    res = tree.query(c_coor,k=min(LIMIT_CLOSEST_POINT,len(base_stations)))

    # print(res[0])
    for c, d, p in zip(clients, res[0], res[1]):
        if d[0] <= base_stations[p[0]].coverage.radius:
            c.base_station = base_stations[p[0]]    
        c.closest_base_stations = [(a, base_stations[b]) for a,b in zip(d,p)]

# Check closest base_stations of a client and assign the closest non-excluded avaliable base_station to the client.
def assign_closest_base_station(client, excludes=None):
    updated_list = []
    for d,b in client.closest_base_stations:
        if b.pk in excludes:
            continue
        d = distance((client.x, client.y), (b.coverage.x, b.coverage.y))
        updated_list.append((d,b))
    updated_list.sort(key = operator.itemgetter(0))
    for d,b in updated_list:
        if d <= b.coverage.radius:
            client.base_station = b
            return
    client.base_station = None

class BSDict:
    bs_dict = {}

class BSMultiPoint:
    bs_points = None

def shapely(client):
    origin = Point(client.x, client.y)
    nearest_geoms = nearest_points(origin, BSMultiPoint.bs_points)
    near_idx0 = nearest_geoms[0]

    near_idx1 = nearest_geoms[1]


    b = BSDict.bs_dict.get((near_idx1.x, near_idx1.y))
    d = near_idx0.distance(near_idx1)

    # print("a = ", near_idx0)
    # print(d)
    # print("b = ", near_idx1)

    if d <= b.coverage.radius:
        client.base_station = b
    else:
        client.base_station = None


def shapely2(client):
    from shapely.ops import nearest_points
    global BS_POINTS
    print(BS_POINTS)
    BS_POINTS = MultiPoint(BS_POINTS)
    print(type(BS_POINTS))

    origin = Point(client.x, client.y)
    print(origin)
    nearest_geoms = nearest_points(origin, BS_POINTS)

    near_idx0 = nearest_geoms[0]

    near_idx1 = nearest_geoms[1]

    # print(nearest_geoms)

    print(near_idx0)
    a = (near_idx0.x, near_idx0.y)
    b = (near_idx1.x, near_idx1.y)
    print(distance(a, b))
    print(near_idx1)

# start = time.time()
# kdtree(origin, dest)
# end = time.time()
# print(end - start)


# print("#-"*30)
#
#
# start = time.time()
# shapely(origin1, dest1)
# end = time.time()
# print(end - start)
