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
        self.connect_attempt = []
        self.block_count = []
        self.handover_count = []
    
    def get_stats(self):
        return (
            self.total_connected_users,
            self.total_used_bw,
            self.avg_slice_load_ratio,
            self.avg_slice_client_count,
            self.coverage_ratio,
            self.block_count,
            self.handover_count,
        )

    def collect(self):
        yield self.env.timeout(0.25)
        self.connect_attempt.append(0)
        self.block_count.append(0)
        self.handover_count.append(0)
        while True:
            self.block_count[-1] /= self.connect_attempt[-1] if self.connect_attempt[-1] != 0 else 1
            self.handover_count[-1] /= self.connect_attempt[-1] if self.connect_attempt[-1] != 0 else 1

            self.total_connected_users.append(self.get_total_connected_users())
            self.total_used_bw.append(self.get_total_used_bw())
            self.avg_slice_load_ratio.append(self.get_avg_slice_load_ratio())
            self.avg_slice_client_count.append(self.get_avg_slice_client_count())
            self.coverage_ratio.append(self.get_coverage_ratio())

            self.connect_attempt.append(0)
            self.block_count.append(0)
            self.handover_count.append(0)
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

    def incr_connect_attempt(self):
        self.connect_attempt[-1] += 1

    def incr_block_count(self):
        self.block_count[-1] += 1

    def incr_handover_count(self):
        self.handover_count[-1] += 1
