class Floor:
    def __init__(self, floor, passenger):
        self.floor = floor
        self.passenger = list(passenger)

    def __str__(self):
        return f"Floor {self.floor}: {self.passenger}"

    def add_passenger(self, passenger):
        """

        :param passenger:
        """
        self.passenger.append(passenger)

    def remove_passenger(self, passenger):
        """

        :param passenger:
        """
        for p in self.passenger:
            if p == passenger:
                self.passenger.remove(passenger)