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
        self.last_usage = 0
        self.action = env.process(self.iter())
        print(self)

    def connect_to_closest_base_station(self):
        self.base_station = None #TODO

    def iter(self):
        print(f'[{self.env.now}] {self}')
        slice = self.base_station.slices[i]

        # Determine usage and if there exists.
        if self.usage_remaining <= 0:
            if self.usage_freq < random.random():
                # Generate a new usage
                self.usage_remaining = self.usage_pattern.generate()
                self.base_station.slices[i].connected_users += 1
                print(f'[{self.env.now}] Client [{self.x}, {self.y}] requests {self.usage_remaining} usage.')
            else:
                # Do nothing
                pass
        else:
            amount = slice.get_consumable_share()
            # Allocate resource and consume ongoing usage with given bandwidth
            slice.capacity.get(amount)
            self.last_usage = amount
            

        yield self.env.timeout(1)

        # Put the resource back
        slice.capacity.put(self.last_usage)

        yield self.env.process(self.iter())

    def get_slice(self):
        return self.base_station.slices[self.connected_slice_index]

    def __str__(self):
        return f'Client [{self.x:<5}, {self.y:>5}] connected to: slice={self.connected_slice_index:<2} @ {self.base_station}\t with mobility pattern of {self.mobility_pattern}'
