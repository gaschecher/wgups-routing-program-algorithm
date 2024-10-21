# WGU Student ID: 012314325

from datetime import datetime, timedelta
import logging
import sys
from .package import Package
from .hash_table import HashTable
from .truck import Truck
from .routing import optimize_routes, clean_address, get_distance
from .data.locations import location_to_address, distance_matrix
from .data.packages import packages

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variables for API access
package_hash = None
trucks = None

# Create the hash table for packages; this includes what is required in the instructions and some additional fields (see packages.py in the data directory for more info).
def create_package_hash_table():
    package_hash = HashTable()
    for package_data in packages:
        address_parts = package_data["Address"].split(", ")
        package = Package(
            package_data["Package ID"],
            clean_address(address_parts[0]),
            address_parts[1],
            address_parts[2].split()[0],
            address_parts[2].split()[1],
            package_data["Delivery Deadline"],
            package_data["Weight KILO"],
            package_data["Truck Number"],
            package_data["Delayed"],
            package_data["Delayed Until"],
            package_data["Group"]
        )
        # Insert each package into the hash table.
        package_hash.insert(package.package_id, package)
    logging.info(f"Created package hash table with {len(packages)} packages")
    return package_hash

def print_package_status(hash_table, time):
    logging.info(f"Printing package status at {time}")
    print(f"\nPackage Status at {time}:")
    for i in range(1, 41):
        package = hash_table.lookup(i)
        if package:
            status = package.get_status(time)
            print(f"Package {package.package_id}: {status}")
            logging.debug(f"Package {package.package_id} status: {status}")

# Simulate deliveries for each truck. I called it simulate_deliveries but in production it would be something like deliver_packages.
def simulate_deliveries(trucks):
    logging.info("Starting delivery simulation")
    current_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    active_trucks = trucks[:2]

    while active_trucks:
        for truck in active_trucks:
            # If the truck has no route, remove it from active trucks. With 3 trucks and 2 drivers, all trucks are loaded before 8:00 AM.
            # Once a truck finishes its route, it's removed, allowing another truck to be deployed, ensuring efficient use of the drivers through continuous truck rotation.

            if not truck.route:
                active_trucks.remove(truck)
                if len(active_trucks) < 2 and trucks[2].packages:
                    trucks[2].time = current_time
                    active_trucks.append(trucks[2])
                continue

            package, distance = truck.route.pop(0)
            if package:
                # Calculate the time required to deliver the package.
                current_time = max(current_time, package.load_time or current_time)
                travel_time = distance / truck.speed
                current_time += timedelta(hours=travel_time)
                truck.time = current_time
                truck.deliver_package(package, distance)
                logging.info(f"Delivered package {package.package_id} at {current_time}. Distance: {distance:.1f} miles, New location: {truck.current_location}")
            else:
                # Return to hub if no package is present, meaning all deliveries are done for the truck.
                travel_time = distance / truck.speed
                current_time += timedelta(hours=travel_time)
                truck.time = current_time
                truck.return_to_hub(distance)

    for truck in trucks:
        logging.info(f"Truck {truck.truck_id} finished at {truck.time}, total mileage: {truck.mileage:.1f}")
        print(f"Truck {truck.truck_id} finished at {truck.time}, total mileage: {truck.mileage:.1f}")

def assign_packages_to_trucks(trucks, packages):
    logging.info("Assigning packages to trucks")
    unassigned_packages = []
    grouped_packages = []
    deadline_packages = []

    for package in packages:
        # Check if the package is assigned to a specific truck, load it directly.
        if package.truck_number:
            trucks[int(package.truck_number) - 1].load_package(package)
        # Check if the package is part of a group that must be delivered together.
        elif package.group:
            grouped_packages.append(package)
        # Check if the package is delayed and assign it to the third truck, since we have 3 trucks and 2 drivers.
        # If we had 2 trucks and 2 drivers, the logic would be different.
        elif package.delayed:
            trucks[2].load_package(package, datetime.strptime(package.delayed_until, "%H:%M"))
        # Check if the package has a delivery deadline, prioritize assigning it.
        elif package.deadline and package.deadline != "":
            deadline_packages.append(package)
        # If none of the above apply, mark it as unassigned for now.
        else:
            unassigned_packages.append(package)

    # Assign grouped packages to the first two trucks if there's enough capacity.
    for package in grouped_packages:
        assigned = False
        for truck in trucks[:2]:
            if len(truck.packages) + len(grouped_packages) <= truck.capacity:
                for p in grouped_packages:
                    truck.load_package(p)
                assigned = True
                break
        if assigned:
            break

    # Assign packages with deadlines based on the shortest route.
    for package in deadline_packages:
        # Calculate the distances to other packages in the first two trucks.
        distances = [sum(get_distance(package.address, p.address) for p in truck.packages) for truck in trucks[:2]]
        # Assign the package to the truck with the shorter distance.
        if not distances[0] and not distances[1]:
            trucks[0].load_package(package)
        elif distances[0] <= distances[1]:
            trucks[0].load_package(package)
        else:
            trucks[1].load_package(package)

    # Assign remaining unassigned packages to the truck with the shortest distance to other packages.
    for package in unassigned_packages:
        distances = [sum(get_distance(package.address, p.address) for p in truck.packages) for truck in trucks]
        # Find the truck with the shortest total distance and check capacity.
        min_distance_index = distances.index(min(distances))
        if len(trucks[min_distance_index].packages) < trucks[min_distance_index].capacity:
            trucks[min_distance_index].load_package(package)
        else:
            # If no trucks have enough capacity, try to assign to any avaliable truck.
            for i in range(3):
                if len(trucks[i].packages) < trucks[i].capacity:
                    trucks[i].load_package(package)
                    break
            else:
                logging.warning(f"Failed to assign package {package.package_id} to any truck")

    logging.info(f"Finished assigning packages. Truck 1: {len(trucks[0].packages)} packages, Truck 2: {len(trucks[1].packages)} packages, Truck 3: {len(trucks[2].packages)} packages")

def initialize_data():
    global package_hash, trucks
    logging.info("Initializing data for WGUPS Routing Program")
    package_hash = create_package_hash_table()

    trucks = [Truck(1), Truck(2), Truck(3)]
    packages = [package_hash.lookup(i) for i in range(1, 41) if package_hash.lookup(i)]

    assign_packages_to_trucks(trucks, packages)

    # Optimize the routes for each truck.
    for truck in trucks:
        truck.current_location = "4001 South 700 East, Salt Lake City, UT 84107" 
        truck.route = optimize_routes([truck], distance_matrix)[truck.truck_id]

    simulate_deliveries(trucks)

    # Calculate and log total mileage.
    total_mileage = sum(truck.mileage for truck in trucks)
    logging.info(f"Total mileage for all trucks: {total_mileage:.1f} miles")
    print(f"Total mileage for all trucks: {total_mileage:.1f} miles")

def main():
    try:
        initialize_data()

        for time_str in ["9:00 AM", "10:00 AM", "1:00 PM"]:
            time = datetime.strptime(time_str, "%I:%M %p").replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
            print_package_status(package_hash, time)

        # Allow user to check the status of individual packages.
        while True:
            package_id = input("\nEnter a package ID to check its status (or 'q' to quit): ")
            if package_id.lower() == 'q':
                break
            try:
                package_id = int(package_id)
                package = package_hash.lookup(package_id)
                if package:
                    print(package)
                    logging.debug(f"User queried package {package_id}: {package}")
                else:
                    print(f"No package found with ID {package_id}")
                    logging.warning(f"User queried non-existent package ID: {package_id}")
            except ValueError:
                print("Please enter a valid package ID")
                logging.warning(f"User entered invalid package ID: {package_id}")

        logging.info("WGUPS Routing Program finished")
    
    except ValueError as e:
        logging.critical(f"Critical error in route calculation: {e}")
        logging.critical("Script execution stopped due to distance calculation error.")
        sys.exit(1)

if __name__ == "__main__":
    main()