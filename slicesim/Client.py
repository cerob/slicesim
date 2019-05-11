import random

from .utils import shapely, assign_closest_base_station


class Client:
    def __init__(self, pk, env, x, y, mobility_pattern,
                 usage_freq, usage_pattern,
                 connected_slice_index, base_station=None):
        self.pk = pk
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
        self.closest_base_stations = []

        # Stats
        self.total_connected_time = 0
        self.total_unconnected_time = 0
        self.total_request_count = 0
        self.total_consume_time = 0
        self.total_usage = 0

        self.action = env.process(self.iter())
        # print(self.usage_freq)

    def connect_to_closest_base_station(self):
        self.base_station = None #TODO

    def iter(self):
        print(f'[{int((self.env.now+1)/2)}] {self}')
        
        if self.base_station is None:
            # Client is not connected to a base station
            self.total_unconnected_time += 0.5

        else:
            # Client is connected to a base station
            slice = self.get_slice()
            self.total_connected_time += 0.5

            if self.env.now % 2 == 0:            
                # Determine usage and if there exists.
                if self.usage_remaining <= 0:
                    if self.usage_freq < random.random():
                        # Generate a new usage
                        self.usage_remaining = self.usage_pattern.generate()
                        slice.connected_users += 1
                        self.total_request_count += 1
                        print(f'[{int(self.env.now/2)}] Client [{self.x}, {self.y}] requests {self.usage_remaining} usage.')
                    else:
                        # Do nothing
                        pass
                else:
                    amount = min(slice.get_consumable_share(), self.usage_remaining)
                    # Allocate resource and consume ongoing usage with given bandwidth
                    slice.capacity.get(amount)
                    print(f'[{int(self.env.now/2)}] Client [{self.x}, {self.y}] gets {amount} usage.')
                    self.last_usage = amount
                    self.usage_remaining -= amount
            
            else:
                # Interphase

                # Put the resource back
                if self.last_usage != 0:
                    slice.capacity.put(self.last_usage)
                    print(f'[{int((self.env.now+1)/2)}] Client [{self.x}, {self.y}] puts back {self.last_usage} usage.')
                    self.total_consume_time += 1
                    self.total_usage += self.last_usage
                    self.last_usage = 0
                
                # Move the client
                x, y = self.mobility_pattern.generate_movement()
                self.x += x
                self.y += y

                # Check for coverage
                if not self.base_station.coverage.is_in_coverage(self.x, self.y):
                    # shapely(self)
                    assign_closest_base_station(self, excludes=[self.base_station.pk])
 
        yield self.env.timeout(1)

        yield self.env.process(self.iter())

    def get_slice(self):
        if self.base_station is None:
            return None
        return self.base_station.slices[self.connected_slice_index]

    def __str__(self):
        return f'Client_{self.pk} [{self.x:<5}, {self.y:>5}] connected to: slice={self.get_slice()} @ {self.base_station}\t with mobility pattern of {self.mobility_pattern}'
