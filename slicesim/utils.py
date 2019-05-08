import math
import random
import time
from shapely.geometry import Point, MultiPoint

origin = [(450,1003), (132,2132)]
dest = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
# origin1 = Point(origin[0], origin[1])
# dest1  = [Point(p[0], p[1]) for p in dest]

origin = [(random.randint(0, 100000), random.randint(0, 100000)) for i in range(500000)]
dest = [(random.randint(0, 100000), random.randint(0, 100000)) for i in range(50000)]

def distance(a, b):
    return math.sqrt(sum((i-j)**2 for i,j in zip(a, b)))

# Initial connections using k-d tree
def kdtree(clients, base_stations):
    from sklearn.neighbors import KDTree

    c_coor = [(c.x,c.y) for c in clients]
    bs_coor = [p.coverage.center for p in base_stations]

    tree = KDTree(bs_coor, leaf_size=2)
    res = tree.query(c_coor)

    for c, d, p in zip(clients, res[0], res[1]):
        if d[0] <= base_stations[p[0]].coverage.radius:
            c.base_station = base_stations[p[0]]


def shapely(origin, dest):

    from shapely.ops import nearest_points

    destinations = MultiPoint(dest)

    nearest_geoms = nearest_points(origin, destinations)

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
