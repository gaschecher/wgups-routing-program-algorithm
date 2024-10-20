# Student ID: 012314325
# WGUPS Routing Program

import csv
from datetime import datetime
from package import Package
from hash_table import HashTable
from truck import Truck
from routing import load_distance_data, optimize_routes

def load_package_data(filename, hash_table):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == "":
                continue
            package = Package(
                int(row[0]), row[1], row[2], row[3], row[4], row[5], float(row[6]), row[7]
            )
            hash_table.insert(package.package_id, package)

def print_package_status(hash_table, time):
    print(f"\nPackage Status at {time}:")
    for i in range(1, 41):  # Assuming package IDs are from 1 to 40
        package = hash_table.lookup(i)
        if package:
            status = package.status
            if status == "Delivered" and package.delivery_time > time:
                status = "En Route"
            elif status == "At Hub" and package.truck is not None:
                status = "En Route"
            print(f"Package {package.package_id}: {status}")

def main():
    package_hash = HashTable()
    load_package_data("data/WGUPS Package File.csv", package_hash)
    distances = load_distance_data("data/WGUPS Distance Table.csv")

    trucks = [Truck(1), Truck(2), Truck(3)]
    packages = [package_hash.lookup(i) for i in range(1, 41) if package_hash.lookup(i)]

    routes = optimize_routes(trucks, packages, distances)

    # Print total mileage
    total_mileage = sum(truck.mileage for truck in trucks)
    print(f"Total mileage for all trucks: {total_mileage:.1f} miles")

    # Print package status at different times
    for time_str in ["9:00 AM", "10:00 AM", "1:00 PM"]:
        time = datetime.strptime(time_str, "%I:%M %p")
        print_package_status(package_hash, time)

    # Interface for checking individual package status
    while True:
        package_id = input("\nEnter a package ID to check its status (or 'q' to quit): ")
        if package_id.lower() == 'q':
            break
        try:
            package_id = int(package_id)
            package = package_hash.lookup(package_id)
            if package:
                print(package)
            else:
                print(f"No package found with ID {package_id}")
        except ValueError:
            print("Please enter a valid package ID")

if __name__ == "__main__":
    main()