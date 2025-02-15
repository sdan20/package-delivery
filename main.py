import datetime
import helper
from truck import Truck


if __name__ == '__main__':
    # Import data from the two CSV files and create Truck objects.
    helper.import_location_distance_data()
    helper.register_packages()
    truck_one = Truck('Truck One')
    truck_two = Truck('Truck Two')

    # Load truck_two and deliver its first round of packages.
    helper.load_truck_two(truck_two)
    while len(truck_two.packages_held) > 0:
        helper.travel_nearest_stop(truck_two)
    helper.travel_to_hub(truck_two)

    # Load truck_one and deliver its first round of packages.
    # The time is set to 9:05 a.m. because packages 6 and 25 are delayed and arrive at the hub at that time.
    truck_one.set_time_on_clock(datetime.timedelta(hours=9, minutes=5))
    helper.load_truck_one(truck_one)
    while len(truck_one.packages_held) > 0:
        helper.travel_nearest_stop(truck_one)
    helper.travel_to_hub(truck_one)

    # Load truck_two and deliver its next round of packages.
    helper.load_truck_two_again(truck_two)
    while len(truck_two.packages_held) > 0:
        helper.travel_nearest_stop(truck_two)
    helper.travel_to_hub(truck_two)

    # Load truck_one and deliver the remaining packages.
    # Package 9, with an incorrect address, will be corrected and loaded, as it should be past 10:20 a.m. by this time.
    helper.load_truck_one_again(truck_one)
    while len(truck_one.packages_held) > 0:
        helper.travel_nearest_stop(truck_one)
    helper.travel_to_hub(truck_one)

    # Run the user interface prompts.
    program_terminated = False
    while not program_terminated:
        selection = ''
        while selection not in ('1', '2', '3'):
            print('\nPlease select an option below:')
            print('1. Print the final status of all packages with total mileage')
            print('2. Print the status of all packages at a specific time')
            print('3. Exit the program')
            selection = input()

        if selection == '3':
            program_terminated = True
            print('\nExiting program...')

        else:
            time = ''
            # Set default values used for selection 1 so that all packages are delivered.
            hours = 23
            minutes = 58

            # Check the time that user inputs to validate that an actual time was entered
            if selection == '2':
                time = ''
                while len(time) < 4:
                    time = input('Please enter a time (HH:MM): ')
                    if ':' not in time:
                        continue
                    colon_index = time.index(':')
                    hours = time[0:colon_index]
                    minutes = time[colon_index + 1:colon_index + 3]
                    if hours.isnumeric() and minutes.isnumeric() and 0 <= int(hours) < 24 and 0 <= int(minutes) < 60:
                        hours = int(hours)
                        minutes = int(minutes)
                        if ('p' in time or 'P' in time) and (hours != 12):  # Includes 'p.m.', meaning the afternoon
                            hours += 12
                    else:
                        time = ''

            # Create a datetime object and call print_status_all_packages()
            time = datetime.timedelta(hours=hours, minutes=minutes)
            helper.print_status_all_packages(time)  # Execute regardless of whether option 1 or 2 was selected
            print()  # Formatting

            # After outputting the final package data, print the total distance traveled by all trucks.
            if selection == '1':
                print(f'Total miles traveled by all trucks: '
                      f'{truck_two.get_distance_traveled() + truck_one.get_distance_traveled()}\n')
