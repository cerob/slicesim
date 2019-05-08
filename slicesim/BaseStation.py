class BaseStation:
    def __init__(self, pk, x, y, coverage, capacity_bandwidth, slices=None):
        self.pk = pk
        self.x = x
        self.y = y
        self.coverage = coverage
        self.capacity_bandwidth = capacity_bandwidth
        self.slices = slices
        print(self)

    def __str__(self):
        return f'BS_{self.pk:<2} [{self.x:<5}, {self.y:>5}]\t cov:{self.coverage}\t with cap {self.capacity_bandwidth:<5}'