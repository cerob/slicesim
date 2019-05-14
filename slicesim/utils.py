import math

from sklearn.neighbors import KDTree as kdt

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

class KDTree:
    last_run_time = 0
    limit = None

    # Initial connections using k-d tree
    @staticmethod
    def run(clients, base_stations, run_at):
        print(f'KDTREE CALL [{run_at}] - limit: {KDTree.limit}')
        if run_at == KDTree.last_run_time:
            return
        KDTree.last_run_time = run_at
        
        c_coor = [(c.x,c.y) for c in clients]
        bs_coor = [p.coverage.center for p in base_stations]

        tree = kdt(bs_coor, leaf_size=2)
        res = tree.query(c_coor,k=min(KDTree.limit,len(base_stations)))

        # print(res[0])
        for c, d, p in zip(clients, res[0], res[1]):
            if d[0] <= base_stations[p[0]].coverage.radius:
                c.base_station = base_stations[p[0]]    
            c.closest_base_stations = [(a, base_stations[b]) for a,b in zip(d,p)]