# Define a Package class which creates and manages packages.
# The delivery status and especially the timestamps for when a status change occurs are important for using the program.
class Package:

    def __init__(self, package_id, address, city, zip_code, deadline, mass):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.deadline = deadline
        self.mass = mass
        self.status = 'at the hub'
        self.picked_up_by = ''
        self.on_truck_time = False
        self.delivery_time = False

    def get_package_id(self):
        return self.package_id

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_deadline(self):
        return self.deadline

    def get_city(self):
        return self.city

    def set_city(self, city):
        self.city = city

    def get_zip_code(self):
        return self.zip_code

    def set_zip_code(self, zip_code):
        self.zip_code = zip_code

    def get_mass(self):
        return self.mass

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_picked_up_by(self):
        return self.picked_up_by

    def set_picked_up_by(self, picked_up_by):
        self.picked_up_by = picked_up_by

    def get_on_truck_time(self):
        return self.on_truck_time

    def set_on_truck_time(self, on_truck_time):
        self.on_truck_time = on_truck_time

    def get_delivery_time(self):
        return self.delivery_time

    def set_delivery_time(self, delivery_time):
        self.delivery_time = delivery_time
