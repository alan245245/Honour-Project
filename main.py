import random

from Elevator import Elevator
from Floor import Floor
from Passenger import Passenger
import csv

# config
config_number_of_floor = 16
config_number_of_passenger = 100
config_elevator_capacity = 10
'''
0, Proposed Algorithm
1, Nearest First
'''
config_elevator_algorithm = 1
config_random_passenger = True
config_preset_passenger = 1
'''
0, spawn passengers spontaneously
1, spawn passengers in real time 
'''
config_real_time = 1

building = []
time = 0

if config_real_time == 0:
    if config_random_passenger:
        for i in range(config_number_of_passenger):
            spawn_floor = random.randint(0, config_number_of_floor - 1)
            target_floor = random.randint(0, config_number_of_floor - 1)
            while spawn_floor == target_floor:
                target_floor = random.randint(0, config_number_of_floor - 1)
            passenger = Passenger(spawn_floor, target_floor)
    else:
        match config_preset_passenger:
            case 0:
                for i in range(config_number_of_floor - 1):
                    for y in range(5):
                        if i != 0:
                            Passenger(0,i)
            case 1:
                for i in range(config_number_of_floor - 1):
                    for y in range(3):
                        if i != 0:
                            Passenger(0, i)
                            Passenger(i, 0)

    for i in range(config_number_of_floor):
        passenger = []
        for p in Passenger.all_passenger:
            if p.currentFloor == i:
                passenger.append(p)
        building.append(Floor(i, passenger))

    for b in building:
        print(b)
elif config_real_time == 1:
    for i in range(config_number_of_floor):
        building.append(Floor(i, []))

elevator = Elevator(config_number_of_floor - 1, config_elevator_algorithm)
# Original Model
match config_real_time:
    case 0:
        while len(Passenger.all_passenger) != len(Passenger.arrived_passenger):
            # Add called floors
            for f in building:
                for p in f.passenger:
                    elevator.add_call_floor(f.floor, p.direction)

            passengerExiting = list()

            # Passenger enter elevator
            for p in building[elevator.currentFloor].passenger:
                if p.direction == elevator.direction: # If the elevator direction matches passenger's direction
                    response = elevator.add_passenger(p)
                    if response:
                        passengerExiting.append(p)
            if len(passengerExiting) > 0:
                Passenger.add_wait_time(2)
            for p in passengerExiting:
                building[elevator.currentFloor].remove_passenger(p)

            elevator.determine_target_floor()

            # Passenger enter elevator
            for p in building[elevator.currentFloor].passenger:
                if p.direction == elevator.direction: # If the elevator direction matches passenger's direction
                    response = elevator.add_passenger(p)
                    if response:
                        passengerExiting.append(p)
            if len(passengerExiting) > 0:
                Passenger.add_wait_time(2)
            for p in passengerExiting:
                building[elevator.currentFloor].remove_passenger(p)

            elevator.remove_passenger() # Passenger exit elevator
            print(elevator)
            print(Passenger.all_passenger)
            elevator.move_to_next_floor()
    case 1:
        elevator_time = 0
        while len(Passenger.all_passenger) <= config_number_of_passenger | len(Passenger.all_passenger) != len(Passenger.arrived_passenger):
            # Roll dice to decide whether passenger will be spawned
            if (random.randint(0,100) >= 75) & (len(Passenger.all_passenger) < config_number_of_passenger):
                generate_passenger = random.randint(1,1)

                # Ensure does not exceed config_number_of_passenger
                if (config_number_of_passenger - len(Passenger.all_passenger) - generate_passenger) < 0:
                    generate_passenger = config_number_of_passenger - len(Passenger.all_passenger)

                # Starts generate passenger
                for i in range(generate_passenger):
                    spawn_floor = random.randint(0, config_number_of_floor - 1)
                    target_floor = random.randint(0, config_number_of_floor - 1)
                    while spawn_floor == target_floor:
                        target_floor = random.randint(0, config_number_of_floor - 1)
                    passenger = Passenger(spawn_floor, target_floor)
                    building[spawn_floor].add_passenger(passenger)

            # Add called floors
            for f in building:
                for p in f.passenger:
                    elevator.add_call_floor(f.floor, p.direction)

            passengerExiting = list()

            if len(Passenger.all_passenger) > 0:
                elevator.determine_target_floor()

            # Passenger enter elevator
            for p in building[elevator.currentFloor].passenger:
                if p.direction == elevator.direction: # If the elevator direction matches passenger's direction
                    response = elevator.add_passenger(p)
                    if response:
                        passengerExiting.append(p)
            if len(passengerExiting) > 0:
                Passenger.add_wait_time(2)
            for p in passengerExiting:
                building[elevator.currentFloor].remove_passenger(p)

            # Passenger enter elevator
            for p in building[elevator.currentFloor].passenger:
                if p.direction == elevator.direction: # If the elevator direction matches passenger's direction
                    response = elevator.add_passenger(p)
                    if response:
                        passengerExiting.append(p)
            if len(passengerExiting) > 0:
                Passenger.add_wait_time(2)
            for p in passengerExiting:
                building[elevator.currentFloor].remove_passenger(p)

            elevator.remove_passenger() # Passenger exit elevator
            print(elevator)
            print(Passenger.all_passenger)
            if elevator_time > 3:
                elevator_time = 0
                elevator.move_to_next_floor()

            time = time + 1
            elevator_time = elevator_time + 1

print("Simulation Complete")
wait_time_sum = 0
travel_time_sum = 0
for p in Passenger.all_passenger:
    wait_time_sum = wait_time_sum + p.waitTime
    travel_time_sum = travel_time_sum + p.travelTime
print(f"Avg Wait Time: {wait_time_sum/ len(Passenger.all_passenger)} | Avg Travel Time: {travel_time_sum/ len(Passenger.all_passenger)}")

with open('simulation_data.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='unix', delimiter=' ',
                            quotechar='\"', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['From', 'To', 'Wait Time', 'Travel Time'])
    for p in Passenger.all_passenger:
        spamwriter.writerow([p.currentFloor, p.targetFloor, p.waitTime, p.travelTime])
        #spamwriter.writerow("From:{} To:{} Wait:{} Travel:{}".format(p.currentFloor, p.targetFloor, p.waitTime, p.travelTime))
