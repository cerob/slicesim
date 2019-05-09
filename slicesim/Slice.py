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
        if self.bandwidth_guaranteed > 0:
            # TODO handle better
            return self.bandwidth_max / self.connected_users
        else:
            return self.bandwidth_max / self.connected_users

    def __str__(self):
        return self.name
