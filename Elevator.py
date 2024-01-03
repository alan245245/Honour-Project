import math
from Passenger import Passenger

class Elevator:
    def __init__(self):
        self.currentFloor = 0
        self.targetFloor = 0
        self.direction = 1
        self.passengers = list()
        self.calledFloor = set()
        # self.highestFloor = floor

    def add_call_floor(self, callFloor, direction):
        """

        :param callFloor:
        :param direction:
        """
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
        passenger.inElevator = True
        self.passengers.append(passenger)

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
            difference = self.currentFloor - f[0] # Calculate the difference between floor
            distance = abs(difference) # Absolute the difference to be distance
            if distance < current_distance:
                # If the current called floor is closer to current floor
                if f[1] == self.direction:
                    # if the called floor has the same direction as current elevator
                    current_distance = distance
                    self.targetFloor = f[0]

        # Reverse direction
        if self.targetFloor == -1:
            self.direction = self.direction * -1 # reverse direction
            self.determine_target_floor()

    def move_to_next_floor(self):
        Passenger.add_wait_time(4)
        if self.direction == 1:
            self.currentFloor = self.currentFloor + 1
        else:
            self.currentFloor = self.currentFloor - 1
