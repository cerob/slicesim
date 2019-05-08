import random


class Client:
    def __init__(self, env, x, y, mobility_pattern,
                 usage_freq, usage_pattern,
                 connected_slice_index, base_station=None):
        self.env = env
        self.x = x
        self.y = y
        self.mobility_pattern = mobility_pattern
        self.usage_freq = usage_freq
        self.usage_pattern = usage_pattern
        self.base_station = base_station
        self.connected_slice_index = connected_slice_index
        self.usage_remaining = 0
        self.action = env.process(self.iter())
        print(self)

    def connect_to_closest_base_station(self):
        self.base_station = None #TODO

    def iter(self):
        print(f'[{self.env.now}] {self}')

        # determine usage and if there exists.
        if self.usage_remaining <= 0:
            if self.usage_freq < random.random():
                # Generate a new usage
                self.usage_remaining = self.usage_pattern.generate()
                print(f'[{self.env.now}] Client [{self.x}, {self.y}] requests {self.usage_remaining} usage.')
            else:
                # Do nothing
                pass
        else:
            # Consume ongoing usage with given bandwidth
            pass

        # allocate resource
        yield self.env.timeout(1)

        # put the resource back
        yield self.env.process(self.iter())

    def get_slice(self):
        return self.base_station.slices[self.connected_slice_index]

    def __str__(self):
        return f'Client [{self.x:<5}, {self.y:>5}] connected to: slice={self.connected_slice_index:<2} @ {self.base_station}\t with mobility pattern of {self.mobility_pattern}'
