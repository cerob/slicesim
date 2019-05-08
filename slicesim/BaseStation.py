class BaseStation:
    def __init__(self, x, y, coverage, capacity_bandwidth, slices=None):
        self.x = x
        self.y = y
        self.coverage = coverage
        self.capacity_bandwidth = capacity_bandwidth
        self.slices = slices