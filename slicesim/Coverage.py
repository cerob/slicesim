import math


class Coverage:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def _get_gaussian_distance(self, p):
        return math.sqrt(sum((i-j)**2 for i,j in zip(p, self.center)))

    def is_in_coverage(self, x, y):
        return self._get_gaussian_distance((x,y)) <= self.radius

    def __str__(self):
        x, y = self.center
        return f'[c=({x:<4}, {y:>4}), r={self.radius:>4}]'