class Client:
    def __init__(self, env, x, y, mobility_pattern, base_station=None):
        self.env = env
        self.x = x
        self.y = y
        self.mobility_pattern = mobility_pattern
        self.base_station = base_station
        print(self)
        self.action = env.process(self.consume())

    def connect_to_closest_base_station(self):
        self.base_station = None #TODO
    
    def consume(self):
        print(f'[{self.env.now}] {self}')


        yield self.env.timeout(1)
        yield self.env.process(self.consume())

    def __str__(self):
        return f'Client [{self.x}, {self.y}]\t connected to: {self.base_station}\t with mobility pattern of {self.mobility_pattern}'
