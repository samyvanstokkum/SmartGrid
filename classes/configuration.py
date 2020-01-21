from house import House
from battery import Battery
import csv
import copy
import random
import matplotlib.pyplot as plt
import time
from hillclimber import HillClimber
from simulatedannealing import SimulatedAnnealing

from helpers import *

class Configuration():
    def __init__(self, type_of_config, district_nr):
        self.type = type_of_config
        self.district_nr = district_nr
        self.district = []
        self.get_district()
        self.batteries = []
        self.get_batteries()
        self.get_configuration()
        self.routes = {}

    def get_district(self):
        """Retrieve all houses from csv and create district with house objects."""

        # open and read the csv file
        f = open(f'data/district{self.district_nr}_houses.csv')
        district_data = csv.reader(f)
        next(district_data)

        # create an object for each house
        for house_id, row in enumerate(district_data, 1):
            x, y = eval(row[0]), eval(row[1])
            power = eval(row[2])
            house = House(house_id, x, y, power)
            self.district.append(house)
    
    def get_batteries(self): 
        """Retrieve batteries from csv and create battery objects."""

        # open and read the csv file
        f = open(f'data/district{self.district_nr}_batteries.csv')
        batteries_data = csv.reader(f)
        next(batteries_data)

        # create an object for each battery
        for battery_id, row in enumerate(batteries_data, 1):
            x, y = eval(row[0])[0], eval(row[0])[1]
            capacity = eval(row[1])
            battery = Battery(battery_id, x, y, capacity)

            self.batteries.append(battery)
    
    
    def get_configuration(self):
        if self.type == "random":
            self.random_algo()
        elif self.type == "greedy":
            self.greedy_algo()
        else: # if type = "cluster"
            self.cluster_algo()
        
    def random_algo(self):

        HOUSES_PER_BATTERY = 30

        while True:
            # t = time.time()
            all_houses = copy.deepcopy(self.district)
            
            for battery in self.batteries:
                battery.restore()

            while all_houses:
                for battery in self.batteries:
                    sample_of_houses = random.sample(all_houses, HOUSES_PER_BATTERY)
                    for house in sample_of_houses:
                        all_houses.remove(house)

                    for house in sample_of_houses:
                        battery.add_house(house)
                    

            satisfing_constraints = []
            for battery in self.batteries:
                if battery.capacity < 0:
                    satisfing_constraints.append(False)
                else: 
                    satisfing_constraints.append(True)

            if all(satisfing_constraints):
                break
            # else:
            #     n = t - time.time()
            #     if round(n) % 10 == 0:
            #         print("Still running...")

            

    def greedy_algo(self):
        houses_to_batteries_distances = get_houses_to_batteries_distances(self.district, self.batteries)

        for house, distances in houses_to_batteries_distances.items():
            
            house_to_batteries_distances = get_house_to_batteries_distances(distances)

            while True:
                # select the route with the smallest distance from house to battery

                battery_nr = min(house_to_batteries_distances, key=house_to_batteries_distances.get)
                battery = self.batteries[battery_nr - 1]

                # check if capacity fits the power
                if battery.capacity - house.power >= 0:
                    battery.add_house(house) 
                    break

                else:
                    # update feasible battery distances
                    del house_to_batteries_distances[battery_nr]
                    if not house_to_batteries_distances:
                        # now we know that no batteries have room for this house
                        self.update_configuration(house, distances)
                        break

    def update_configuration(self, house, distances):
        remaining_house = house

        remaining_capacity = {}
        for battery_nr, battery in enumerate(self.batteries, 1):
            remaining_capacity[battery_nr] = battery.capacity

        house_to_batteries_distances = get_house_to_batteries_distances(distances)
        
        max_capacity_battery_nr = max(remaining_capacity, key=remaining_capacity.get)
        max_capacity_battery = self.batteries[max_capacity_battery_nr - 1]

        swap_options = []
        while not swap_options:
            desired_battery_nr = min(house_to_batteries_distances, key=house_to_batteries_distances.get)
            desired_battery = self.batteries[desired_battery_nr - 1]
            del house_to_batteries_distances[desired_battery_nr] # TODO: MISSCHIEN EEN TRY-EXCEPT

            for house in desired_battery.houses:
                if house.power < remaining_capacity[max_capacity_battery_nr] and house.power + remaining_capacity[desired_battery_nr] > remaining_house.power:
                    # save these houses and the costs of swapping
                    distance_desired = abs(house.x - desired_battery.x) + abs(house.y - desired_battery.y)
                    distance_max_capacity = abs(house.x - max_capacity_battery.x) + abs(house.y - max_capacity_battery.y)
                    distance_difference = distance_max_capacity - distance_desired
                    swap_options.append((house, distance_difference))
                
        # check lowest cost for swapping and swap
        house_to_extract = min(swap_options, key=lambda x: x[1])[0]

        # house swaps
        desired_battery.remove_house(house_to_extract)
        desired_battery.add_house(remaining_house)
        max_capacity_battery.add_house(house_to_extract)

        
    def cluster_algo(self):
        pass

    def make_plot(self):
        self.get_routes()
        colors = ['r', 'b', 'k', 'g', 'm']
        plt.figure()
        for battery in self.batteries:
            plt.plot(battery.x, battery.y, 'H')
            for house in battery.houses:
                plt.plot(house.x, house.y, 'k*')
            
        i = 0
        for battery in self.batteries:
            for x, y in self.routes[battery]:
                plt.plot(x, y, colors[i])
            i += 1
        plt.show()


    def get_routes(self, share_grid = False):
        for battery in self.batteries:
            self.routes[battery] = []
            for house in battery.houses:
                A = get_coordinates(house, battery)
                self.routes[battery].append(A)


if __name__ == "__main__":
    config1 = Configuration("greedy", 1)
    # HillClimber(config1.batteries, "steepest", 1000)
    HillClimber(config1.batteries, 'stochastic', 1000)
    for battery in config1.batteries:
        print(battery.houses)
    config1.make_plot()

    
    
    