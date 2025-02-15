import datetime
from helper import HUB_INDEX


class Truck:
    """A class used to represent a delivery truck.

    Attributes:
        name (str): The name of the truck.
        location_index (int): An index to retrieve information on the current location from tables in helper.py.
        packages_held (obj:`list` of :obj:`Package`): A list of currently held packages.
        distance_traveled (float): The total number of units (miles) traveled.
        time_on_clock (time): The current time, which is checked or updated at each stop.
        capacity (int): The max number of packages that can be held at one time.
        speed (float): The average speed, in mph, of a truck at work.

    """

    def __init__(self, name, time_on_clock=datetime.timedelta(hours=8, minutes=0)):
        """Construct a Truck object.

        Args:
            name (str): The name of the truck.
            time_on_clock (:obj:`time`, optional): The current time. Defaults to 8:00 a.m.

        """
        self.name = name
        self.location_index = HUB_INDEX
        self.packages_held = []
        self.distance_traveled = 0.0
        self.time_on_clock = time_on_clock
        self.capacity = 16
        self.speed = 18.0


    def get_name(self):
        return self.name

    def get_location_index(self):
        return self.location_index

    def set_location_index(self, location_index):
        self.location_index = location_index

    def get_packages_held(self):
        return self.packages_held

    def get_distance_traveled(self):
        return self.distance_traveled

    def get_time_on_clock(self):
        return self.time_on_clock

    def get_capacity(self):
        return self.capacity

    def get_speed(self):
        return self.speed

    def set_time_on_clock(self, time_on_clock):
        self.time_on_clock = time_on_clock


    def load_package(self, package):
        """Load a Package object into the packages_held and update the Package object.

        Args:
            package (Package): The package object to save and modify.

        Returns:
            None.
        """
        package.set_status('en route')
        package.set_time_loaded(self.time_on_clock)
        package.set_assigned_truck(self.name)
        self.packages_held.append(package)


    def deliver_package(self, package):
        """Deliver a Package object and update its status.

        Args:
            package (Package): The package object to save and modify.

        Returns:
            None.

        """
        package.set_status('delivered')
        package.set_time_delivered(self.time_on_clock)
        self.packages_held.remove(package)


    def update_distance_traveled(self, distance_traveled):
        """Update distanced traveled by Truck object.

        Args:
            distance_traveled (float): The number of miles to record.

        Returns:
            None.

        """
        self.distance_traveled += distance_traveled
        hours = distance_traveled / self.speed  # Fractional hour quantity
        self.time_on_clock += datetime.timedelta(hours=hours)
