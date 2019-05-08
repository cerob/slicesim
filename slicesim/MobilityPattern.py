class MobilityPattern:
    def __init__(self, name, distribution, *dist_params):
        self.name = name
        self.distribution = distribution
        self.dist_params = dist_params

    def generate_movement(self):
        x = self.distribution(*self.dist_params)
        y = self.distribution(*self.dist_params)
        return x, y
