import datetime

from package import Package

# Global variables
total_packages = 40         # Total number of packages to be delivered
package_hash_table = []     # Hash table for storing all packages
distance_table = []         # Table to store data from 'WGUPS Distance Table.csv'

# Copy of package 9's bad address so that the incorrect address can be recalled. Data will be added later.
package_9_bad_address = [(datetime.timedelta(hours=10, minutes=20))]

# Avoid collisions when working with the hash table. Items are appended to indexes, rather than assigned.
for i in range(total_packages):
    package_hash_table.append([])


# Determines where in the hash table a key and value will be placed.
# This is used to add items and to find their positions later.
def hash_key(key):
    return hash(key) % len(package_hash_table)


# Imports data from 'WGUPS Package File.csv', creates package objects, and adds them to package_hash_table.
def import_packages():
    with open('WGUPS Package File.csv', mode='r') as file:
        # Read package data from CSV file and retrieve them as a list of lines.
        raw_data = file.readlines()

        # Ignore lines without package data, which are simply for spacing and column labels.
        line = 0
        while raw_data[line][0] != '1':
            line += 1

        # Iterate through all lines of package data and create package objects.
        for line_i in range(line, len(raw_data)):
            line_data = raw_data[line_i].split(',')
            package = Package(line_data[0], line_data[1], line_data[2], line_data[4], line_data[5], line_data[6])

            # Add the key and package as a list in that index. Collisions are avoided, as items are appended to a list.
            key = package.get_package_id()
            package_hash_table[hash_key(key)].append([key, package])


# Removes the zip code and extra space from the address where it is found in 'WGUPS Distance Table.csv'
def remove_zip_code(address):
    index = address.index('(') - 1
    return address[0:index]


# Imports data from 'WGUPS Distance Table.csv', updates distance_table for easy reference, and cleans up formatting.
def import_distances():
    with open('WGUPS Distance Table.csv', mode='r') as file:
        # Ignore data that will not be part of the distance table.
        # The first row is also not needed, as the same information is found in the first data column.
        raw_data = file.readlines()
        line_found = False
        line = 0

        # Find the first line of relevant data in the csv file
        while not line_found:
            test_data = raw_data[line].split(',')
            if len(test_data) > 3 and test_data[2] == '0':
                line_found = True
            else:
                line += 1

        # This blank list makes it easy to copy addresses later. The first cell is above addresses, so it must be empty.
        # This design ensures that each address is at index [0,i] and [i,0] for every instance of i (every address).
        # [1,0] and [0,1] both hold the address of the hub.
        distance_table.append([''])
        for line_i in range(line, len(raw_data)):
            line_data = raw_data[line_i].split(',')
            line_data.pop(0)
            row_data = []
            for col_i in range(len(line_data)):
                row_data.append(line_data[col_i])
            distance_table.append(row_data)

        # Iterate through all the addresses (the first item in each row) and remove zip code.
        for address_i in range(1, len(distance_table)):
            address = remove_zip_code(distance_table[address_i][0])
            distance_table[address_i][0] = address
            distance_table[0].append(address)  # Copy addresses to the first row which holds addresses as column headers

    return distance_table


# Looks up and returns a package for a given package ID.
def get_package(package_id):
    index_data = package_hash_table[hash_key(package_id)]
    for d in index_data:
        if d[0] == package_id:
            return d[1]


# Adds a first load of packages to truck two, based on deadlines and which packages must be on truck two.
def load_truck_two(truck):
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


# Adds a first load of packages to truck one, based on deadlines.
# This truck leaves the hub at 9:05 a.m., after all packages have arrived at the hub.
def load_truck_one(truck):
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


# Adds a second load of packages to truck two.
def load_truck_two_again(truck):
    truck.load_package(get_package('2'))
    truck.load_package(get_package('10'))
    truck.load_package(get_package('11'))
    truck.load_package(get_package('12'))
    truck.load_package(get_package('17'))
    truck.load_package(get_package('22'))
    truck.load_package(get_package('23'))
    truck.load_package(get_package('33'))  # Shares destination with package 2


# Adds a second load of packages to truck one. This marks loading all remaining packages that were at the hub.
# Package 9 is included, which had an incorrect address saved, so it is updated at time of loading.
def load_truck_one_again(truck):
    package_9 = get_package('9')
    package_9_bad_address.append(package_9.get_address())
    package_9_bad_address.append(package_9.get_city())
    package_9_bad_address.append(package_9.get_zip_code())
    package_9.set_address('410 S State St')
    package_9.set_city('Salt Lake City')
    package_9.set_zip_code('84111')
    truck.load_package(package_9)          # Delivery address can be updated at 10:20 a.m.
    truck.load_package(get_package('24'))
    truck.load_package(get_package('27'))
    truck.load_package(get_package('35'))  # Shares destination with package 27


# Determines the closest stop that the truck needs to make, then the truck travels there and delivers a package.
# Every address in the stored distance_table is checked to see if a package needs to be delivered there.
# Potential stop addresses and the distances are saved and compared to select the closest location.
def travel_closest_stop(truck):
    current_location = truck.get_location()
    location_index = distance_table[0].index(current_location)
    # This list will store all addresses for which a truck must still deliver a held package.
    potential_stops = []

    # This list will contain tuples of address-distance pairs.
    stops_distance = []

    # Copy the delivery address for each package that still needs to be delivered.
    for package in truck.get_packages_held():
        potential_stops.append(package.get_address())

    # Retrieve the distance from the current location to each potential location from the distance table.
    # This begins with row 2 because 0 is a blank space, and 1 only compares the hub location to itself.
    for table_index in range(2, len(distance_table)):

        # Use the row where the current_location is found to retrieve distance data.
        if table_index < location_index:
            address = distance_table[0][table_index]
            if address in potential_stops:
                stops_distance.append((address, distance_table[location_index][table_index]))

        # Use the column where current_location is found to retrieve distance data.
        else:
            address = distance_table[table_index][0]
            if address in potential_stops:
                stops_distance.append((address, distance_table[table_index][location_index]))  # Stores data as a tuple.

    closest_distance = 1000  # A huge distance which is far beyond the bounds of what could be traveled within a region.
    closest_stop = ''
    for stop, distance in stops_distance:  # Unpack the tuple.
        distance = float(distance)
        if distance < closest_distance:
            closest_distance = distance
            closest_stop = stop
    truck.add_distance_traveled(closest_distance)
    truck.set_location(closest_stop)

    # Deliver all held packages that are intended for the truck's new location.
    for package in truck.get_packages_held():
        if package.get_address() == closest_stop:
            truck.deliver_package(package)


# This takes a truck from its current location to the hub location.
# It compares the location of current_location with the location of the hub, using the distance table.
def travel_to_hub(truck):
    current_location = truck.get_location()
    location_index = distance_table[0].index(current_location)

    distance_to_hub = float(distance_table[location_index][1])  # Hub data is stored at column 1
    truck.set_location(truck.hub)
    truck.add_distance_traveled(distance_to_hub)


# Obtains the status of all packages and prints it to the screen.
# This cycles through the package ID numbers and prints the related information for one package per loop iteration.
def print_status_all_packages(time):
    package_id = 0
    print('\nDisplaying data...')
    print('Package ID, Address, City, Zip Code, Delivery Deadline, Mass in Kilograms, Status, Delivery Time')

    while package_id < total_packages:
        package_id += 1
        package = get_package(str(package_id))
        delivery_time = package.get_delivery_time()

        if package_id == 9 and time < package_9_bad_address[0]:
            address = package_9_bad_address[1]
            city = package_9_bad_address[2]
            zip_code = package_9_bad_address[3]
        else:
            address = package.get_address()
            city = package.get_city()
            zip_code = package.get_zip_code()

        if delivery_time > time:                       # Package has not been delivered
            if package.get_on_truck_time() > time:     # Package has not yet been loaded
                delivery_status = 'at the hub'
                delivery_time = ''
            else:                                      # Package has been loaded onto a truck but not yet delivered
                delivery_status = f'en route - on {package.get_picked_up_by()}'
                delivery_time = ''
        else:                                          # Package has been delivered
            delivery_status = f'{package.get_status()} by {package.get_picked_up_by()}'
            delivery_time = ', ' + str(delivery_time)  # For formatting
        print(f'{package.get_package_id()}, {address}, {city}, {zip_code},'
              f' {package.get_deadline()}, {package.get_mass()}, {delivery_status}{delivery_time}')
