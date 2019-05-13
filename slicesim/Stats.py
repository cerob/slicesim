class Stats:
    def __init__(self, env, base_stations, clients):
        self.env = env
        self.base_stations = base_stations
        self.clients = clients
        #self.graph = graph

        # Stats
        self.total_connected_users = []
        self.total_used_bw = []
        self.avg_slice_load_ratio = []
        self.avg_slice_client_count = []
        self.coverage_ratio = []
    
    def get_stats(self):
        return (
            self.total_connected_users,
            self.total_used_bw,
            self.avg_slice_load_ratio,
            self.avg_slice_client_count,
            self.coverage_ratio,
        )

    def collect(self):
        yield self.env.timeout(0.25)
        while True:
            self.total_connected_users.append(self.get_total_connected_users())
            self.total_used_bw.append(self.get_total_used_bw())
            self.avg_slice_load_ratio.append(self.get_avg_slice_load_ratio())
            self.avg_slice_client_count.append(self.get_avg_slice_client_count())
            self.coverage_ratio.append(self.get_coverage_ratio())

            #self.graph.draw_all(*self.get_stats())
            yield self.env.timeout(1)

    def get_total_connected_users(self):
        t = 0
        for c in self.clients:
            t += c.connected
        # for bs in self.base_stations:
        #     for sl in bs.slices:
        #         t += sl.connected_users
        return t

    def get_total_used_bw(self):
        t = 0
        for bs in self.base_stations:
            for sl in bs.slices:
                t += sl.capacity.capacity - sl.capacity.level
        return t

    def get_avg_slice_load_ratio(self):
        t, c = 0, 0
        for bs in self.base_stations:
            for sl in bs.slices:
                c += sl.capacity.capacity
                t += sl.capacity.capacity - sl.capacity.level
                #c += 1
                #t += (sl.capacity.capacity - sl.capacity.level) / sl.capacity.capacity
        return t/c if c !=0 else None

    def get_avg_slice_client_count(self):
        t, c = 0, 0
        for bs in self.base_stations:
            for sl in bs.slices:
                c += 1
                t += sl.connected_users
        return t/c if c !=0 else None
    
    def get_coverage_ratio(self):
        t, cc = 0, 0
        for c in self.clients:
            cc += 1
            if c.base_station is not None and c.base_station.coverage.is_in_coverage(c.x, c.y):
                t += 1
        return t/cc if cc !=0 else None




# TODO
# block count
# handover event
# average mobility
