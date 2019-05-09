class Slice:
    #TODO make some vars static
    def __init__(self, name, ratio,
                 connected_users, user_share, delay_tolerance, qos_class,
                 bandwidth_guaranteed, bandwidth_max, init_capacity):
        self.name = name
        self.connected_users = connected_users
        self.user_share = user_share
        self.delay_tolerance = delay_tolerance
        self.qos_class = qos_class
        self.ratio = ratio
        self.bandwidth_guaranteed = bandwidth_guaranteed
        self.bandwidth_max = bandwidth_max
        self.init_capacity = init_capacity
        self.capacity = 0
    
    def get_consumable_share(self):
        real_cap = min(self.init_capacity, self.bandwidth_max)

        if self.bandwidth_guaranteed > 0:
            # TODO handle better
            return real_cap / self.connected_users
        else:
            return real_cap / self.connected_users

    def __str__(self):
        return f'{self.name:<10} init={self.init_capacity:<5} cap={self.capacity.level:<5} diff={(self.init_capacity - self.capacity.level):<5}'
