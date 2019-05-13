import operator
import random

from .utils import shapely, distance


class Client:
    def __init__(self, pk, env, x, y, mobility_pattern,
                 usage_freq, usage_pattern,
                 subscribed_slice_index, base_station=None):
        self.pk = pk
        self.env = env
        self.x = x
        self.y = y
        self.mobility_pattern = mobility_pattern
        self.usage_freq = usage_freq
        self.usage_pattern = usage_pattern
        self.base_station = base_station
        self.subscribed_slice_index = subscribed_slice_index
        self.usage_remaining = 0
        self.last_usage = 0
        self.closest_base_stations = []
        self.connected = False

        # Stats
        self.total_connected_time = 0
        self.total_unconnected_time = 0
        self.total_request_count = 0
        self.total_consume_time = 0
        self.total_usage = 0

        self.action = env.process(self.iter())
        # print(self.usage_freq)

    def iter(self):
        #print(f'[{int((self.env.now+1)/2)}] {self}')
        
        if self.base_station is None:
            # TODO
            # Client is not connected to a base station
            self.total_unconnected_time += 0.5

        else:
            # Client is connected to a base station
            self.total_connected_time += 0.5

            if self.env.now % 2 == 0:
                # Determine usage and if there exists.
                if self.usage_remaining <= 0:
                    if self.usage_freq < random.random():
                        # Generate a new usage
                        self.usage_remaining = self.usage_pattern.generate()
                        self.total_request_count += 1
                        print(f'[{int(self.env.now/2)}] Client_{self.pk} [{self.x}, {self.y}] requests {self.usage_remaining} usage.')
                    else:
                        # Do nothing
                        pass
                
                if self.connected:
                    self.consume_start()
                else:
                    self.connect()
                       
            else:
                # Interphase

                self.consume_finish()
                
                if self.usage_remaining <= 0:
                    self.disconnect()

        if self.env.now % 2 == 1:
            # Move the client
            x, y = self.mobility_pattern.generate_movement()
            self.x += x
            self.y += y

            # Check for coverage
            if self.base_station is None:
                self.assign_closest_base_station()
            elif not self.base_station.coverage.is_in_coverage(self.x, self.y):
                self.disconnect()
                # shapely(self)
                self.assign_closest_base_station(excludes=[self.base_station.pk])

        yield self.env.timeout(1)

        yield self.env.process(self.iter())

    def get_slice(self):
        if self.base_station is None:
            return None
        return self.base_station.slices[self.subscribed_slice_index]
    
    def connect(self):
        # TODO handover
        slice = self.get_slice()
        if self.connected:
            return
        if slice.is_avaliable():
            slice.connected_users += 1
            self.connected = True
            print(f'[{int(self.env.now/2)}] Client_{self.pk} [{self.x}, {self.y}] connected to slice={self.get_slice()} @ {self.base_station}')
            return True
        else:
            # TODO log block
            print(f'[{int(self.env.now/2)}] Client_{self.pk} [{self.x}, {self.y}] connection refused to slice={self.get_slice()} @ {self.base_station}')
            return False

    def disconnect(self):
        if self.connected == False:
            print(f'[{int(self.env.now/2)}] Client_{self.pk} [{self.x}, {self.y}] is already disconnected from slice={self.get_slice()} @ {self.base_station}')
        else:
            slice = self.get_slice()
            slice.connected_users -= 1
            self.connected = False
            print(f'[{int(self.env.now/2)}] Client_{self.pk} [{self.x}, {self.y}] disconnected from slice={self.get_slice()} @ {self.base_station}')
        return not self.connected

    def consume_start(self):
        slice = self.get_slice()
        amount = min(slice.get_consumable_share(), self.usage_remaining)
        # Allocate resource and consume ongoing usage with given bandwidth
        slice.capacity.get(amount)
        print(f'[{int(self.env.now/2)}] Client_{self.pk} [{self.x}, {self.y}] gets {amount} usage.')
        self.last_usage = amount
        self.usage_remaining -= amount

    def consume_finish(self):
        slice = self.get_slice()
        # Put the resource back
        if self.last_usage != 0:
            slice.capacity.put(self.last_usage)
            print(f'[{int((self.env.now+1)/2)}] Client_{self.pk} [{self.x}, {self.y}] puts back {self.last_usage} usage.')
            self.total_consume_time += 1
            self.total_usage += self.last_usage
            self.last_usage = 0

    # Check closest base_stations of a client and assign the closest non-excluded avaliable base_station to the client.
    def assign_closest_base_station(self, excludes=None):
        updated_list = []
        for d,b in self.closest_base_stations:
            if b.pk in excludes:
                continue
            d = distance((self.x, self.y), (b.coverage.x, b.coverage.y))
            updated_list.append((d,b))
        updated_list.sort(key = operator.itemgetter(0))
        for d,b in updated_list:
            if d <= b.coverage.radius:
                self.base_station = b
                return
        self.base_station = None

    def __str__(self):
        return f'Client_{self.pk} [{self.x:<5}, {self.y:>5}] connected to: slice={self.get_slice()} @ {self.base_station}\t with mobility pattern of {self.mobility_pattern}'
