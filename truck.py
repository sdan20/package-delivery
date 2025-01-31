import datetime


# This class defines, creates, and manages all truck objects.
# A truck is used to move packages from the central hub to their delivery destinations.
# It also keeps track of time, as each package has a delivery deadline, although some deadlines are simply end of day.
class Truck:

    capacity = 16  # Max packages that can be held at a time
    speed = 18     # Miles per hour
    hub = '4001 South 700 East'

    # A truck object stores its location, which packages are held, distance traveled in miles, and the time.
    def __init__(self, name, time_on_clock=datetime.timedelta(hours=8, minutes=0)):
        self.location = self.hub
        self.packages_held = []
        self.distance_traveled = 0
        self.name = name
        self.time_on_clock = time_on_clock

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location

    def get_packages_held(self):
        return self.packages_held

    # Loads a package onto the truck object and updates its status accordingly.
    def load_package(self, package):
        package.set_status('en route')  # This does not matter in the program's current implementation
        package.set_on_truck_time(self.time_on_clock)
        package.set_picked_up_by(self.name)
        self.packages_held.append(package)

    # Delivers/removes a package from the truck object and updates its status accordingly.
    def deliver_package(self, package):
        package.set_status('delivered')
        package.set_delivery_time(self.time_on_clock)
        self.packages_held.remove(package)

    def get_distance_traveled(self):
        return self.distance_traveled

    # Updates distance traveled and the time, which is based on miles traveled.
    def add_distance_traveled(self, distance_traveled):
        self.distance_traveled += distance_traveled
        hours = distance_traveled / self.speed  # Fractional hour quantity for time adjustment
        self.time_on_clock += datetime.timedelta(hours=hours)

    def get_time_on_clock(self):
        return self.time_on_clock

    def set_time_on_clock(self, time_on_clock):
        self.time_on_clock = time_on_clock
