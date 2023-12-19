import random

from Floor import Floor
from Passenger import Passenger

# config
number_of_floor = 6
number_of_passenger = 3

building = []
all_passenger = []

for i in range(number_of_passenger):
    passenger = Passenger(0, 5)
    all_passenger.append(passenger)

for i in range(number_of_floor):
    passenger = []
    for p in all_passenger:
        if p.currentFloor == i:
            passenger.append(p)
    building.append(Floor(i, passenger))

for b in building:
    print(b)

for p in building[0].passenger:
    if p.targetFloor == 3:
        temp = building[0].remove_passenger(p)
        print(temp)
