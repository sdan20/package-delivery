import datetime
import sympy
from package import Package


# Global variables are used throughout this file.
num_packages = 0         # Total number of packages handled
package_hash_table = []  # All Package objects
HUB_INDEX = 0            # Index of hub is [0][0] in distance and address tables

# All distance data in a 2D array. Each index refers to the same location on both axes.
# The table is a pyramid, row 0 only saves index 0, and each subsequent row saves an additional value (or column).
distance_table = []

# All address data in a 2D array (index matches index of distance_table).
# Columns store location name (0), street address (1), city (2), state (3), zip code (4), and intended packages (5).
full_address_table = []

# Copy of package 9's bad address so that the incorrect address can be recalled. Data will be added later.
package_9_bad_address = [(datetime.timedelta(hours=10, minutes=20))]


def get_package(package_id):
    """Return a Package object for a given package id, by accessing package_hash_table."""
    index_data = package_hash_table[hash_key(package_id)]
    # Find the object, knowing that multiple objects may be saved at the same index.
    for d in index_data:
        if d[0] == package_id:
            return d[1]


def hash_key(key):
    """Return a hash key for storing and retrieving data in package_hash_table."""
    return hash(key) % len(package_hash_table)


def import_location_distance_data():
    """Read, clean, format, and save distance and location data from a CSV file."""
    with open('WGUPS Distance Table.csv', mode='r') as file:
        raw_distance_data = file.readlines()
    first_row = None
    for row in range(len(raw_distance_data)):
        row_data = raw_distance_data[row].split(',')
        # Data rows have at least three columns to indicate a location name, location address, and distance value.
        # A street address must have three or more characters, or at least contain 'HUB'.
        if len(row_data) < 3 or len(row_data[1]) < 3:
            continue
        elif row_data[1][-3:] == 'HUB' and row_data[2] == '0':
            # HUB must be in the first data row.
            first_row = row
            break

    if not first_row:
        print('The specified file cannot be used. Please review the user guide to correct its format.')
    else:
        table_row = 0
        for row in range(first_row, len(raw_distance_data)):
            row_data = raw_distance_data[row].split(',')
            loc_name = row_data.pop(0)
            address = row_data.pop(0)
            full_address_table.append([loc_name, address])
            # Table has the same number of columns and rows, and each subsequent row has one additional data column.
            distance_table.append([])
            # Save all distance data to the table; indexes serve as ids.
            for col in range(table_row + 1):
                distance_table[table_row].append(float(row_data[col]))
            table_row += 1


def count_packages():
    """Return package data rows from CSV file."""
    global num_packages
    with open('WGUPS Package File.csv', mode='r') as file:
        # Read package data from file and retrieve them as a list of lines.
        raw_data = file.readlines()
    # Ignore lines without package data, which are simply for spacing and column labels.
    first_row = 0
    while raw_data[first_row][0] != '1':
        first_row += 1
    num_packages = len(raw_data) - first_row

    return raw_data, first_row


def prepare_hash_table():
    """Assign least 1.3 times the expected number of objects as buckets to hash table (the closest prime number)."""
    num_buckets = int(num_packages * 1.3)
    while not sympy.isprime(num_buckets):
        num_buckets += 1
    # Manage collisions when working with the hash table by appending, rather than assigning, objects to indexes.
    for i in range(num_buckets):
        package_hash_table.append([])


def update_address_data(address_data):
    """Format address data and update full_address_table.

    Match addresses from address_data and full_address_table with a unique zip code and street address combination. On
    first access, or match, of this address, full_address_table is updated with provided data. Ids for packages
    intended for this address are saved as a list to full_address_table.

    Args:
        address_data (:obj:`list` of :obj:`str`): The full address of a relevant location, with an id at index 0.

    Returns:
        The index of the address for data retrieval from full_address_table and distance_table.

    """
    package_id = address_data[0]
    street = address_data[1]
    zip_code = address_data[4]
    for a in range(len(full_address_table)):
        if len(full_address_table[a]) == 2:  # Not yet updated
            a_street = full_address_table[a][1][:-8]
            a_zip_code = full_address_table[a][1][-6:-1]
            if zip_code == a_zip_code and street == a_street:
                full_address_table[a][1] = street
                full_address_table[a].extend(address_data[2:5])
                full_address_table[a].append([package_id])
                return a
        else:                                # Format already updated
            if zip_code == full_address_table[a][4] and street == full_address_table[a][1]:
                # Track packages (by package_id) for this same address.
                full_address_table[a][5].append(package_id)
                return a
    return -1


def register_packages():
    """Create Package objects from read data and add them to package_hash_table."""
    raw_data, first_row = count_packages()  # Unpack tuple
    prepare_hash_table()

    # Iterate through all rows of package data and create Package objects.
    for row in range(first_row, len(raw_data)):
        package_data = raw_data[row].split(',')
        address_index = update_address_data(package_data[:5])
        package = Package(package_data[0], address_index, package_data[5], package_data[6], package_data[7])

        # Append a list of the key and package to the list at its assigned index, to manage collisions.
        key = package.get_package_id()
        package_hash_table[hash_key(key)].append([key, package])


def load_truck_two(truck):
    """Add a first load of packages to truck two, based on deadlines and which packages must be on truck two."""
    truck.load_package(get_package('3'))   # Must be on truck 2
    truck.load_package(get_package('5'))   # Shares destination with packages 37 and 38
    truck.load_package(get_package('13'))  # Must be delivered with specific others - Deadline 10:30
    truck.load_package(get_package('14'))  # Must be delivered with specific others - Deadline 10:30
    truck.load_package(get_package('15'))  # Must be delivered with specific others - Deadline 9:00
    truck.load_package(get_package('16'))  # Must be delivered with specific others - Deadline 10:30
    truck.load_package(get_package('18'))  # Must be on truck 2
    truck.load_package(get_package('19'))  # Must be delivered with specific others
    truck.load_package(get_package('20'))  # Must be delivered with specific others - Deadline 10:30
    truck.load_package(get_package('21'))  # Shares address with package 20
    truck.load_package(get_package('34'))  # Deadline 10:30 - Shares destination with packages 15 and 16
    truck.load_package(get_package('36'))  # Must be on truck 2
    truck.load_package(get_package('37'))  # Deadline 10:30 - Shares destination with package 38
    truck.load_package(get_package('38'))  # Must be on truck 2 - Shares destination with package 37
    truck.load_package(get_package('39'))  # Shares destination with package 13


def load_truck_one(truck):
    """Adds a first load of packages to truck one, departing at 9:05 a.m. so that all packages are ready."""
    truck.load_package(get_package('1'))   # Deadline 10:30
    truck.load_package(get_package('4'))   # Shares destination with package 40
    truck.load_package(get_package('6'))   # Deadline 10:30 - Delayed - Arrives at hub 9:05
    truck.load_package(get_package('7'))   # Shares destination with package 29
    truck.load_package(get_package('8'))   # Shares destination with package 30
    truck.load_package(get_package('25'))  # Deadline 10:30 - Delayed - Arrives at hub 9:05
    truck.load_package(get_package('26'))  # Shares destination with package 25
    truck.load_package(get_package('28'))  # Delayed - Arrives at hub 9:05
    truck.load_package(get_package('29'))  # Deadline 10:30
    truck.load_package(get_package('30'))  # Deadline 10:30
    truck.load_package(get_package('31'))  # Deadline 10:30
    truck.load_package(get_package('32'))  # Delayed - Arrives at hub 9:05 - Shares destination with package 31
    truck.load_package(get_package('40'))  # Deadline 10:30


def load_truck_two_again(truck):
    truck.load_package(get_package('2'))
    truck.load_package(get_package('10'))
    truck.load_package(get_package('11'))
    truck.load_package(get_package('12'))
    truck.load_package(get_package('17'))
    truck.load_package(get_package('22'))
    truck.load_package(get_package('23'))
    truck.load_package(get_package('33'))  # Shares destination with package 2


# Package 9 is included, which had an incorrect address saved, so it is updated at time of loading.
def load_truck_one_again(truck):
    package_9 = get_package('9')
    # package_9_bad_address.append(package_9.get_address())
    # package_9_bad_address.append(package_9.get_city())
    # package_9_bad_address.append(package_9.get_zip_code())
    # package_9.set_address('410 S State St')
    # package_9.set_city('Salt Lake City')1
    # package_9.set_zip_code('84111')
    truck.load_package(package_9)          # Delivery address can be updated at 10:20 a.m.
    truck.load_package(get_package('24'))
    truck.load_package(get_package('27'))
    truck.load_package(get_package('35'))  # Shares destination with package 27


"""Find cell data where the table appears like a pyramid, and rows and columns mirror each other."""
def access_pyramid_table(table, current_cell_id, target_cell_id):
    if target_cell_id < current_cell_id:
        target_data = table[current_cell_id][target_cell_id]  # Locate cell by current row
    else:
        target_data = table[target_cell_id][current_cell_id]  # Locate cell by current column

    return target_data


"""
Travel to the closest address related to a package on the truck and deliver all packages for that stop.
"""
def travel_nearest_stop(truck):
    current_location_index = truck.get_location_index()
    # List to reference the best next stop location, current location, and  package numbers intended for that address.
    closest_stop_data = None

    for package in truck.get_packages_held():
        potential_location_index = package.get_address_index()
        potential_location_distance = access_pyramid_table(distance_table,
                                                            current_location_index, potential_location_index)
        if not closest_stop_data or potential_location_distance < closest_stop_data[1]:
            closest_stop_data = [potential_location_index, potential_location_distance, [package.get_package_id()]]
        elif potential_location_distance == closest_stop_data[1]:
            closest_stop_data[2].append(package.get_package_id())

    truck.set_location_index(closest_stop_data[0])
    truck.update_distance_traveled(closest_stop_data[1])
    for p in closest_stop_data[2]:
        truck.deliver_package(get_package(p))


def travel_to_hub(truck):
    """Travel to hub and update distance traveled and time."""
    distance_to_hub = distance_table[truck.get_location_index()][HUB_INDEX]
    truck.set_location_index(HUB_INDEX)
    truck.update_distance_traveled(distance_to_hub)


def print_status_all_packages(time):
    """Print status of all packages at a given time."""
    package_id = 0
    print('\nDisplaying data...')
    print('Package ID, Address, City, Zip Code, Delivery Deadline, Mass in Kilograms, Status, Delivery Time')

    while package_id < num_packages:
        package_id += 1
        package = get_package(str(package_id))
        delivery_time = package.get_time_delivered()

        #FIXME if package_id == 9 and time < package_9_bad_address[0]:
        #    address = package_9_bad_address[1]
        #    city = package_9_bad_address[2]
        #    zip_code = package_9_bad_address[3]
        #else:

        address = full_address_table[package.get_address_index()][1:5]
        print(address)
        street = address[0]
        city = address[1]
        zip_code = address[3]

        if delivery_time > time:                  # Package not delivered
            if package.get_time_loaded() > time:  # Package not loaded
                delivery_status = 'at the hub'
                delivery_time = ''
            else:                                 # Package loaded
                delivery_status = f'en route - on {package.get_assigned_truck()}'
                delivery_time = ''
        else:                                     # Package delivered
            delivery_status = f'{package.get_status()} by {package.get_assigned_truck()}'
            delivery_time = ', ' + str(delivery_time)
        print(f'{package.get_package_id()}, {street}, {city}, {zip_code},'
              f' {package.get_deadline()}, {package.get_mass()}, {delivery_status}{delivery_time}')
