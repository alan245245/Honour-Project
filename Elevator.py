import math
from Passenger import Passenger


class Elevator:
    def __init__(self, floor, algorithm):
        self.currentFloor = 0
        self.targetFloor = 0
        self.direction = 1
        self.passengers = list()
        self.calledFloor = set()
        self.topFloor = floor
        self.capacity = 10
        self.algorithm = algorithm

    def add_call_floor(self, callFloor, direction):
        """

        :param callFloor:
        :param direction:
        """
        if self.currentFloor == callFloor & self.direction == direction:
            return

        self.calledFloor.add((callFloor, direction))

    def remove_call_floor(self, callFloor, direction):
        """

        :param callFloor:
        :param direction:
        """
        self.calledFloor.discard((callFloor, direction))

    def add_passenger(self, passenger):
        """

        :param passenger:
        """
        if len(self.passengers) >= self.capacity:
            return False
        else:
            passenger.inElevator = True
            self.remove_call_floor(self.currentFloor, self.direction)
            self.passengers.append(passenger)
            return True

    def remove_passenger(self):
        """
        Look for passenger inside the elevator to remove and return a list of passengers
        :rtype: list
        """
        passenger_exiting = list()
        for p in self.passengers:
            if p.reach_target(self.currentFloor):
                passenger_exiting.append(p)
        for p in passenger_exiting:
            self.passengers.remove(p)
        if len(passenger_exiting) > 0:
            Passenger.add_wait_time(2)

        return passenger_exiting

    def determine_target_floor(self):
        match self.algorithm:
            case 0:
                current_distance = math.inf
                self.targetFloor = -1
                # Loop through all passengers in the lift
                for p in self.passengers:
                    difference = p.targetFloor - self.currentFloor
                    distance = abs(difference)
                    if distance < current_distance:
                        # If the passenger floor is closer to current floor
                        current_distance = distance
                        self.targetFloor = p.targetFloor

                # Loop through all called floor
                for f in self.calledFloor:
                    difference = self.currentFloor - f[0]  # Calculate the difference between floor
                    distance = int(abs(difference))  # Absolute the difference to be distance
                    if self.is_in_current_path(f[0]) & self.has_passenger():
                        if distance < current_distance:
                            # If the current called floor is closer to current floor
                            if f[1] == self.direction:
                                # if the called floor has the same direction as current elevator
                                current_distance = distance
                                self.targetFloor = f[0]
                    elif self.has_passenger() == False:
                        if distance < current_distance:
                            # If the current called floor is closer to current floor
                            if f[1] == self.direction:
                                # if the called floor has the same direction as current elevator
                                current_distance = distance
                                self.targetFloor = f[0]

                # Reverse direction if no target found
                if self.targetFloor == -1:
                    self.direction = self.direction * -1  # reverse direction
                    self.determine_target_floor()

                if self.targetFloor > self.currentFloor:
                    self.direction = 1
                elif self.targetFloor < self.currentFloor:
                    self.direction = -1

            case 1:
                current_distance = math.inf
                self.targetFloor = -1
                # Loop through all passengers in the lift
                for p in self.passengers:
                    difference = p.targetFloor - self.currentFloor
                    distance = abs(difference)
                    if distance < current_distance:
                        # If the passenger floor is closer to current floor
                        current_distance = distance
                        self.targetFloor = p.targetFloor

                    # Loop through all called floor
                for f in self.calledFloor:
                    if self.has_passenger():
                        break
                    difference = self.currentFloor - f[0]  # Calculate the difference between floor
                    distance = int(abs(difference))  # Absolute the difference to be distance
                    if (distance < current_distance):
                        # If the current called floor is closer to current floor
                        current_distance = distance
                        self.direction = f[1]
                        self.targetFloor = f[0]

                if self.targetFloor > self.currentFloor:
                    self.direction = 1
                elif self.targetFloor < self.currentFloor:
                    self.direction = -1

    def move_to_next_floor(self):
        if self.currentFloor == self.targetFloor:
            if self.currentFloor == 0:
                self.direction = 1
            return
        Passenger.add_wait_time(4)
        if self.direction == 1:
            self.currentFloor = self.currentFloor + 1
            if self.currentFloor == self.topFloor:
                self.direction = self.direction * -1
        else:
            self.currentFloor = self.currentFloor - 1
            if self.currentFloor < 0:
                self.currentFloor = 0
                self.direction = self.direction * -1
                print("WARNING: Elevator reaches floor smaller than 0")

    def is_in_current_path(self, target_floor):
        if target_floor == -1:
            return False
        difference = self.currentFloor - target_floor
        if difference > 0 & self.direction == -1:
            # if positive and elevator moving downward
            return True
        elif difference <= 0 & self.direction == -1:
            # if negative and elevator moving upward
            return True
        else:
            return False

    def has_passenger(self):
        if len(self.passengers) > 0:
            return True
        else:
            return False

    def __str__(self):
        return f"Elevator at {self.currentFloor} going {self.direction} to {self.targetFloor} with {len(self.passengers)} Passengers"
