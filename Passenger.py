class Passenger:
    all_passenger = list()
    arrived_passenger = list()

    def __init__(self, currentFloor, targetFloor):
        self.targetFloor = targetFloor
        self.currentFloor = currentFloor
        self.arrived = False
        self.waitTime = 0
        self.travelTime = 0

        if targetFloor > currentFloor:
            self.direction = 1
        else:
            self.direction = -1
        self.all_passenger.append(self)

    def add_wait_time(self, time):
        self.waitTime = self.waitTime + time

    def add_travel_time(self, time):
        self.travelTime = self.travelTime + time

    def reach_target(self, floor):
        if floor == self.targetFloor:
            return True
        else:
            return False

    def __str__(self):
        if self.arrived:
            return f"Passenger arrived to {self.targetFloor} from {self.currentFloor}. W: {self.waitTime} T: {self.travelTime}"
        else:
            return f"Passenger need to go {self.direction} from {self.currentFloor} to {self.targetFloor}. W: {self.waitTime} T: {self.travelTime}"

    def __repr__(self):
        return self.__str__()
