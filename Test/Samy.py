# Libraries
import csv
import matplotlib.pyplot as plt

# Classes
from house import House
from battery import Battery
from route import Route

# Functions
from distance import get_distance
from csv import import_district, import_batteries


def main():
    district = import_district(1)
    batteries = import_batteries(1)
    # matrix = make_distance_matrix(district, batteries)

    # set to 1 if you want to print the houses and batteries
    yes_plot = False

    # print batteries and houses
    if yes_plot:
        plt.figure()
        colors = ['r', 'b', 'g', 'c', 'y']
        # plot batteries in red and houses in blue
        for battery in batteries.values():
            plt.plot(battery.x, battery.y,
                     colors[battery.id-1]+'o', markersize=10, label='batteries')

        plt.plot(x_houses, y_houses, 'k*', label='houses')

        # plt.title('houses and batteries')
        plt.grid(True)
        plt.legend(loc='upper center', ncol=10, fontsize=8)

    # append house to battery
    cable_distance, battery_id, house_id = 0, 0, 1
    for battery in batteries.values():
        while battery.capacity - district[house_id].usage >= 0:
            battery.add_house(district[house_id])
            route = battery.calculate_route(district[house_id])
            plt.plot(route[0], route[1], colors[battery_id])

            cable_distance += matrix[house_id-1][battery_id]
            house_id += 1
        battery_id += 1
    # print(cable_distance*9 + 5*5000)

    plt.show()


if __name__ == "__main__":
    main()