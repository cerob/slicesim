class Coverage:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def _get_gaussian_distance(self, p):
        return math.sqrt(sum((i-j)**2 for i,j in zip(p, self.center)))

    def is_in_coverage(self, x, y):
        return _get_gaussian_distance((x,y)) <= self.radius

    def __str__(self):
        return f'[center={self.center}, r={self.radius}]'