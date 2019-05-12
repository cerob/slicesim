class Stats:
    def __init__(self, env, base_stations):
        self.env = env
        self.base_stations = base_stations

        # Stats
        self.total_connected_users = []
        self.total_used_bw = []
        self.avg_slice_load_ratio = []
        self.avg_slice_client_count = []
    
    def get_stats(self):
        return (
            self.total_connected_users,
            self.total_used_bw,
            self.avg_slice_load_ratio,
            self.avg_slice_client_count,
        )

    def collect(self):
        yield self.env.timeout(0.5)
        while True:
            self.total_connected_users.append(self.get_total_connected_users())
            self.total_used_bw.append(self.get_total_used_bw())
            self.avg_slice_load_ratio.append(self.get_avg_slice_load_ratio())
            self.avg_slice_client_count.append(self.get_avg_slice_client_count())
            yield self.env.timeout(2)

    def get_total_connected_users(self):
        t = 0
        for bs in self.base_stations:
            for sl in bs.slices:
                t += sl.connected_users
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
                c += 1
                t += (sl.capacity.capacity - sl.capacity.level) / sl.capacity.capacity
        return t/c if c !=0 else None

    def get_avg_slice_client_count(self):
        t, c = 0, 0
        for bs in self.base_stations:
            for sl in bs.slices:
                c += 1
                t += sl.connected_users
        return t/c if c !=0 else None


# TODO
# in coverage ratio
# block count
# drop count
