class Slice:
    #TODO make some vars static
    def __init__(self, name, ratio,
                 connected_users, delay_tolerance, qos_class,
                 bandwidth_guaranteed, bandwidth_max, init_capacity):
        self.name = name
        self.connected_users = connected_users
        self.delay_tolerance = delay_tolerance
        self.qos_class = qos_class
        self.ratio = ratio
        self.bandwidth_guaranteed = bandwidth_guaranteed
        self.bandwidth_max = bandwidth_max
        self.init_capacity = init_capacity
        self.capacity = 0
