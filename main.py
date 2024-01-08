import random

from Elevator import Elevator
from Floor import Floor
from Passenger import Passenger

# config
number_of_floor = 6
number_of_passenger = 1

building = []
all_passenger = []

for i in range(number_of_passenger):
    passenger = Passenger(0, 2)
    all_passenger.append(passenger)
    passenger = Passenger(0, 1)
    all_passenger.append(passenger)
    passenger = Passenger(2, 0)
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

elevator = Elevator(number_of_floor - 1)
while len(Passenger.all_passenger) != len(Passenger.arrived_passenger):
    # Add called floors
    for f in building:
        for p in f.passenger:
            elevator.add_call_floor(f.floor, p.direction)

    elevator.determine_target_floor()
    elevator.remove_passenger() # Passenger exit elevator
    passengerExiting = list()

    # Passenger enter elevator
    for p in building[elevator.currentFloor].passenger:
        if p.direction == elevator.direction: # If the elevator direction matches passenger's direction
            elevator.add_passenger(p)
            passengerExiting.append(p)
    if len(passengerExiting) > 0:
        Passenger.add_wait_time(2)
    for p in passengerExiting:
        building[elevator.currentFloor].remove_passenger(p)

    print(elevator)
    elevator.move_to_next_floor()
    print(Passenger.all_passenger)