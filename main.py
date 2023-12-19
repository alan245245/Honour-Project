import random

from Elevator import Elevator
from Floor import Floor
from Passenger import Passenger

# config
number_of_floor = 3
number_of_passenger = 3

building = []
all_passenger = []

for i in range(number_of_passenger):
    passenger = Passenger(0, 2)
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

elevator = Elevator()
while len(Passenger.all_passenger) != len(Passenger.arrived_passenger):
    print(elevator.currentFloor)
    for p in building[elevator.currentFloor].passenger:
        if p.direction == elevator.direction:
            elevator.add_passenger(p)
            building[elevator.currentFloor].remove_passenger(p)
    elevator.determine_target_floor()
    elevator.move_to_next_floor()
    for p in elevator.passengers:
        p.add_wait_time(4)
    print(Passenger.all_passenger)
    print(elevator.remove_passenger())
