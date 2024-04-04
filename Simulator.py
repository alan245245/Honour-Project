from Passenger import Passenger
from Elevator import Elevator
from Floor import Floor
import csv
import random
import numpy as np
from scipy.stats import poisson

building = []

def pre_generate_passenger(mode, preset, number_of_passengers, number_of_floor):
    """
    Function to generate passenger from simulator start.
    """
    if mode == 'random':
        for i in range(number_of_passengers):
            spawn_floor = random.randint(0, number_of_floor - 1)
            target_floor = random.randint(0, number_of_floor - 1)
            while spawn_floor == target_floor:
                target_floor = random.randint(0, number_of_floor - 1)
            passenger = Passenger(spawn_floor, target_floor)
    else:
        match preset:
            case 'Morning Rush':
                for i in range(number_of_floor - 1):
                    for y in range(5):
                        if i != 0:
                            Passenger(i, 0)
            case 'Evening Rush':
                for i in range(number_of_floor - 1):
                    for y in range(5):
                        if i != 0:
                            Passenger(0, i)

    for i in range(number_of_floor):
        passenger = []
        for p in Passenger.all_passenger:
            if p.currentFloor == i:
                passenger.append(p)
        building.append(Floor(i, passenger))

    for b in building:
        print(b)

def clear_simulator_data():
    """
    Function to clear all passenger
    """
    Passenger.all_passenger.clear()
    Passenger.arrived_passenger.clear()
    building.clear()

def start_static_simulation(passenger_mode, preset, number_of_passengers, number_of_floor, elevator_algorithm, csv_enabled, csv_file, batch_no):
    """
    Function to start simulation with non real time passenger generation
    """
    for y in range(batch_no):
        clear_simulator_data()
        elevator = Elevator(number_of_floor - 1, elevator_algorithm)
        pre_generate_passenger(passenger_mode, preset, number_of_passengers, number_of_floor)

        # Start simulation loop until all passenger reached destination
        while len(Passenger.all_passenger) != len(Passenger.arrived_passenger):
            # Add called floors
            for f in building:
                for p in f.passenger:
                    elevator.add_call_floor(f.floor, p.direction)

            passengerExiting = list()

            # Passenger enter elevator
            for p in building[elevator.currentFloor].passenger:
                if p.direction == elevator.direction:  # If the elevator direction matches passenger's direction
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
                if p.direction == elevator.direction:  # If the elevator direction matches passenger's direction
                    response = elevator.add_passenger(p)
                    if response:
                        passengerExiting.append(p)
            if len(passengerExiting) > 0:
                Passenger.add_wait_time(2)
            for p in passengerExiting:
                building[elevator.currentFloor].remove_passenger(p)

            elevator.remove_passenger()  # Passenger exit elevator
            print(elevator)
            elevator.move_to_next_floor()
            Passenger.add_wait_time(4)

        print(f"Simulation End")
        print(Passenger.all_passenger)
        wait_time_sum = 0
        travel_time_sum = 0
        for p in Passenger.all_passenger:
            wait_time_sum = wait_time_sum + p.waitTime
            travel_time_sum = travel_time_sum + p.travelTime
        print(f"Avg Wait Time: {wait_time_sum / len(Passenger.all_passenger)} | Avg Travel Time: {travel_time_sum / len(Passenger.all_passenger)}")

        if csv_enabled:
            with open(f'{csv_file}.csv', 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, dialect='unix', delimiter=' ',
                                        quotechar='\"', quoting=csv.QUOTE_MINIMAL)
                if y == 0:
                    spamwriter.writerow(['From', 'To', 'Wait Time', 'Travel Time'])

                for p in Passenger.all_passenger:
                    spamwriter.writerow([p.currentFloor, p.targetFloor, p.waitTime, p.travelTime])
                    # spamwriter.writerow("From:{} To:{} Wait:{} Travel:{}".format(p.currentFloor, p.targetFloor, p.waitTime, p.travelTime))

def start_real_time_simulation(number_of_passengers, number_of_floor, elevator_algorithm, csv_enabled, csv_file, batch_no):
    """
    Function to start simulation with real time passenger generation
    """
    k = np.arange(0, 18)
    cdf = poisson.cdf(k, mu=7)
    cdf = np.round(cdf, 3)
    for y in range(batch_no):
        clear_simulator_data()
        for i in range(number_of_floor):
            building.append(Floor(i, []))
        elevator = Elevator(number_of_floor - 1, elevator_algorithm)
        time = 0
        p_time = 0
        elevator_time = 0
        while len(Passenger.all_passenger) <= number_of_passengers | len(Passenger.all_passenger) != len(
                Passenger.arrived_passenger):
            # Roll dice to decide whether passenger will be spawned
            dice = random.random() <= cdf[np.clip(time - p_time, 0, 17)]
            if (dice) & (len(Passenger.all_passenger) < number_of_passengers):
                generate_passenger = random.randint(1, 1)
                p_time = time

                # Ensure does not exceed number_of_passengers
                if (number_of_passengers - len(Passenger.all_passenger) - generate_passenger) < 0:
                    generate_passenger = number_of_passengers - len(Passenger.all_passenger)

                # Starts generate passenger
                for i in range(generate_passenger):
                    spawn_floor = random.randint(0, number_of_floor - 1)
                    target_floor = random.randint(0, number_of_floor - 1)
                    while spawn_floor == target_floor:
                        target_floor = random.randint(0, number_of_floor - 1)
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
                if p.direction == elevator.direction:  # If the elevator direction matches passenger's direction
                    response = elevator.add_passenger(p)
                    if response:
                        passengerExiting.append(p)
            if len(passengerExiting) > 0:
                Passenger.add_wait_time(1)
                time = time + 1
            for p in passengerExiting:
                building[elevator.currentFloor].remove_passenger(p)

            # Passenger enter elevator
            for p in building[elevator.currentFloor].passenger:
                if p.direction == elevator.direction:  # If the elevator direction matches passenger's direction
                    response = elevator.add_passenger(p)
                    if response:
                        passengerExiting.append(p)
            if len(passengerExiting) > 0:
                Passenger.add_wait_time(1)
                time = time + 1
            for p in passengerExiting:
                building[elevator.currentFloor].remove_passenger(p)

            elevator.remove_passenger()  # Passenger exit elevator
            # print(Passenger.all_passenger)
            if elevator_time > 3:
                elevator_time = 0
                print(elevator)
                elevator.move_to_next_floor()

            Passenger.add_wait_time(1)
            time = time + 1
            elevator_time = elevator_time + 1
        print(f"Simulation End. Simulated {time} Seconds.")
        print(Passenger.all_passenger)
        wait_time_sum = 0
        travel_time_sum = 0
        for p in Passenger.all_passenger:
            wait_time_sum = wait_time_sum + p.waitTime
            travel_time_sum = travel_time_sum + p.travelTime
        print(f"Avg Wait Time: {wait_time_sum / len(Passenger.all_passenger)} | Avg Travel Time: {travel_time_sum / len(Passenger.all_passenger)}")
        if csv_enabled:
            with open(f'{csv_file}.csv', 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, dialect='unix', delimiter=' ',
                                        quotechar='\"', quoting=csv.QUOTE_MINIMAL)
                if y == 0:
                    spamwriter.writerow(['From', 'To', 'Wait Time', 'Travel Time'])

                for p in Passenger.all_passenger:
                    spamwriter.writerow([p.currentFloor, p.targetFloor, p.waitTime, p.travelTime])