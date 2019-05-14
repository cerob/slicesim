class Container:
    def __init__(self, init, capacity):
        self.capacity = capacity
        self.level = init
    
    def get(self, amount):
        if amount <= self.level:
            self.level -= amount
            return True
        else:
            return False

    def put(self, amount):
        if amount + self.level <= self.capacity:
            self.level += amount
            return True
        else:
            return False
