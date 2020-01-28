
class Battery:
    def __init__(self, battery_id, x, y, capacity, cost=5000):
        self.id = battery_id
        self.x = x
        self.y = y
        self.capacity = capacity
        self.houses = []
        self.nr_houses = len(self.houses)
        self.costs = cost

    # add a house objecy to the battery
    def add_house(self, house):
        self.houses.append(house)
        self.capacity -= house.power
        self.houses = sorted(self.houses, key=lambda x: x.id)

    # remove a house object from the battery
    def remove_house(self, house):
        self.houses.remove(house)
        self.capacity += house.power
        self.houses = sorted(self.houses, key=lambda x: x.id)

    def restore(self):
        self.houses.clear()
        self.capacity = 1507.0

    def __repr__(self):
        return f"Battery {self.id}"