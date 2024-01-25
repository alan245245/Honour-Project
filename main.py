import random

from Elevator import Elevator
from Floor import Floor
from Passenger import Passenger
import csv

# config
config_number_of_floor = 6
config_number_of_passenger = 6

building = []
all_passenger = []

for i in range(config_number_of_passenger):
    spawn_floor = random.randint(0, config_number_of_floor - 1)
    target_floor = random.randint(0, config_number_of_floor - 1)
    while spawn_floor == target_floor:
        target_floor = random.randint(0, config_number_of_floor - 1)
    passenger = Passenger(spawn_floor, target_floor)
    all_passenger.append(passenger)

for i in range(config_number_of_floor):
    passenger = []
    for p in all_passenger:
        if p.currentFloor == i:
            passenger.append(p)
    building.append(Floor(i, passenger))

for b in building:
    print(b)

elevator = Elevator(config_number_of_floor - 1)
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
print("Simulation Complete")

with open('simulation_data.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel', delimiter=' ',
                            quotechar='\t', quoting=csv.QUOTE_MINIMAL)
    for p in Passenger.all_passenger:
        spamwriter.writerow("From:{} To:{} Wait:{} Travel:{}".format(p.currentFloor, p.targetFloor, p.waitTime, p.travelTime))
