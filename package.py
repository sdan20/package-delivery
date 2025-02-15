class Package:
    """A class used to represent a package.

    Attributes:
        package_id (str): An id to reference the package.
        address_index (int): An index to reference address and distance information from tables in helper.py.
        deadline (time): The delivery deadline for the package.
        mass (str): The weight, in pounds, of the package.
        special (str): A special note or delivery requirement for the package (or an empty str).
        status (str): The delivery status of the package.
        assigned_truck (str): The name of the truck delivering the package.
        time_loaded (time): The timestamp of when the package was loaded to its truck.
        time_delivered (time): The timestamp of when the package was delivered to its destination.

    """

    def __init__(self, package_id, address_index, deadline, mass, special):
        """Construct a Package object.

        Args:
            package_id (str): An id corresponding to the package.
            address_index (int): An index for use in pulling location and distance data from tables in helper.py.
            deadline (time): The delivery deadline for the package.
            mass (str): The weight, in pounds, of the package.
            special (str): A special note or delivery requirement for the package (or '')

        """
        self.package_id = package_id
        self.address_index = address_index
        self.deadline = deadline
        self.mass = mass
        self.special = special
        self.status = 'at the hub'
        self.assigned_truck = ''
        self.time_loaded = None
        self.time_delivered = None


    def get_package_id(self):
        return self.package_id

    def get_address_index(self):
        return self.address_index

    def set_address_index(self, address_index):
        self.address_index = address_index

    def get_deadline(self):
        return self.deadline

    def set_deadline(self, deadline):
        self.deadline = deadline

    def get_mass(self):
        return self.mass

    def set_mass(self, mass):
        self.mass = mass

    def get_special(self):
        return self.special

    def set_special(self, special):
        self.special = special

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_assigned_truck(self):
        return self.assigned_truck

    def set_assigned_truck(self, assigned_truck):
        self.assigned_truck = assigned_truck

    def get_time_loaded(self):
        return self.time_loaded

    def set_time_loaded(self, time_loaded):
        self.time_loaded = time_loaded

    def get_time_delivered(self):
        return self.time_delivered

    def set_time_delivered(self, time_delivered):
        self.time_delivered = time_delivered
