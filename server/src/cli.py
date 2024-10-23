# cli.py
import argparse
from datetime import datetime, timedelta
import sys
from typing import List
import logging

# Import from your modules
from hash_table import HashTable
from package import Package
from truck import Truck
from routing import optimize_routes, clean_address, get_distance
from data.locations import location_to_address, distance_matrix
from data.packages import packages

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CLI:
    def __init__(self, package_hash, trucks):
        self.package_hash = package_hash
        self.trucks = trucks

    def parse_time(self, time_str: str) -> datetime:
        """Parse time string into datetime object."""
        try:
            formats = [
                "%I:%M %p",  # 9:25 AM
                "%H:%M",     # 13:25
                "%I:%M%p",   # 9:25AM (no space)
                "%H:%M:%S"   # 13:25:00
            ]
            
            for fmt in formats:
                try:
                    parsed_time = datetime.strptime(time_str.strip(), fmt)
                    return datetime.now().replace(
                        hour=parsed_time.hour,
                        minute=parsed_time.minute,
                        second=0,
                        microsecond=0
                    )
                except ValueError:
                    continue
            raise ValueError(f"Time '{time_str}' is not in a valid format")
        except Exception as e:
            print(f"Error parsing time: {e}")
            return None

    def show_single_package_status(self, package_id: int, time_point: datetime):
        """Display status of a specific package at a given time."""
        package = self.package_hash.lookup(package_id)
        if package:
            status = package.get_status(time_point)
            deadline = package.deadline if package.deadline else "EOD"
            print(f"\nPackage Status at {time_point.strftime('%I:%M %p')}")
            print("=" * 80)
            print(f"Package ID: {package_id}")
            print(f"Status: {status}")
            print(f"Address: {package.address}")
            print(f"City: {package.city}")
            print(f"State: {package.state}")
            print(f"ZIP: {package.zip_code}")
            print(f"Delivery Deadline: {deadline}")
            print(f"Weight: {package.weight} kg")
            
            if status == "Delivered":
                print(f"Delivery Time: {package.delivery_time.strftime('%I:%M %p')}")
            elif status == "En Route":
                print(f"Departure Time: {package.en_route_time.strftime('%I:%M %p')}")
            elif status == "At Hub":
                if package.delayed:
                    print(f"Delayed Until: {package.delayed_until}")
                else:
                    print("Status: Awaiting departure")
        else:
            print(f"No package found with ID {package_id}")

    def show_all_packages_status(self, start_time: datetime, end_time: datetime):
        """Display status of all packages within a time range."""
        print(f"\nPackage Status Report: {start_time.strftime('%I:%M %p')} to {end_time.strftime('%I:%M %p')}")
        print("=" * 80)

        for truck in self.trucks:
            # Get all packages ever assigned to this truck
            truck_packages = set()
            for _, _, package in truck.package_history:
                truck_packages.add(package.package_id)
            
            if truck_packages:  # Only show trucks that have packages assigned
                print(f"\nTruck {truck.truck_id}")
                print("-" * 80)
                
                # For each package, find its status within the time range
                for package_id in sorted(truck_packages):
                    package = self.package_hash.lookup(package_id)
                    if package:
                        status = package.get_status(end_time)
                        event_time = ""
                        
                        if status == "Delivered" and package.delivery_time and start_time <= package.delivery_time <= end_time:
                            event_time = package.delivery_time.strftime('%I:%M %p')
                        elif status == "En Route" and package.en_route_time and start_time <= package.en_route_time <= end_time:
                            event_time = package.en_route_time.strftime('%I:%M %p')
                        elif status == "At Hub":
                            if package.delayed and package.delayed_until and datetime.strptime(package.delayed_until, "%H:%M").time() > start_time.time():
                                status = "Delayed"
                                event_time = package.delayed_until
                            else:
                                event_time = start_time.strftime('%I:%M %p')

                        deadline = package.deadline if package.deadline else "EOD"
                        
                        # Print package details in a cleaner format
                        print(f"\nPackage ID: {package.package_id}")
                        print(f"Status: {status}")
                        if status == "Delivered":
                            print(f"Delivery Time: {event_time}")
                        elif status == "Delayed":
                            print(f"Delayed Until: {event_time}")
                        elif status == "En Route":
                            print(f"Departure Time: {event_time}")
                        else:
                            print(f"Current Time: {event_time}")
                        print(f"Delivery Deadline: {deadline}")
                        print(f"Address: {package.address}")
                        print(f"City: {package.city}")
                        print(f"State: {package.state}")
                        print(f"ZIP: {package.zip_code}")
                        if status == "Delivered":
                            print(f"Actual Delivery Time: {package.delivery_time.strftime('%I:%M %p')}")
                
                print("-" * 80)  # Separator between trucks

    def show_total_mileage(self, time_point: datetime):
        """Display total mileage for all trucks at a specific time."""
        print(f"\nMileage Report at {time_point.strftime('%I:%M %p')}")
        print("=" * 50)
        total_mileage = 0
        for truck in self.trucks:
            mileage = truck.get_mileage_at_time(time_point)
            total_mileage += mileage
            print(f"Truck {truck.truck_id}: {mileage:.1f} miles")
        print("-" * 50)
        print(f"Total mileage: {total_mileage:.1f} miles")

    def run_interactive(self):
        """Run interactive mode."""
        while True:
            print("\nWGUPS Package Tracking System")
            print("=" * 30)
            print("1. Look up a single package")
            print("2. View all packages within a time range")
            print("3. Check total mileage")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '4':
                print("\nExiting WGUPS Package Tracking System. Goodbye!")
                break
                
            if choice == '1':
                try:
                    package_id = int(input("Enter package ID (1-40): "))
                    if not 1 <= package_id <= 40:
                        print("Package ID must be between 1 and 40.")
                        continue
                    time_str = input("Enter time to check (e.g., '9:00 AM'): ")
                    time_point = self.parse_time(time_str)
                    if time_point:
                        self.show_single_package_status(package_id, time_point)
                except ValueError:
                    print("Invalid input. Package ID must be a number between 1 and 40.")

            elif choice == '2':
                start_time_str = input("Enter start time (e.g., '8:35 AM'): ")
                end_time_str = input("Enter end time (e.g., '9:25 AM'): ")
                start_time = self.parse_time(start_time_str)
                end_time = self.parse_time(end_time_str)
                if start_time and end_time:
                    if start_time <= end_time:
                        self.show_all_packages_status(start_time, end_time)
                    else:
                        print("Start time must be before end time.")

            elif choice == '3':
                time_str = input("Enter time to check mileage (e.g., '10:00 AM'): ")
                time_point = self.parse_time(time_str)
                if time_point:
                    self.show_total_mileage(time_point)
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

    def run(self):
        """Run the CLI interface."""
        self.run_interactive()

def initialize_delivery_system():
    """Initialize the delivery system and return the hash table and trucks."""
    # Create package hash table
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
        package_hash.insert(package.package_id, package)

    # Initialize trucks
    trucks = [Truck(1), Truck(2), Truck(3)]
    all_packages = [package_hash.lookup(i) for i in range(1, 41) if package_hash.lookup(i)]

    # Assign packages to trucks
    unassigned_packages = []
    grouped_packages = []
    deadline_packages = []

    for package in all_packages:
        if package.truck_number:
            trucks[int(package.truck_number) - 1].load_package(package)
        elif package.group:
            grouped_packages.append(package)
        elif package.delayed:
            trucks[2].load_package(package, datetime.strptime(package.delayed_until, "%H:%M"))
        elif package.deadline and package.deadline != "":
            deadline_packages.append(package)
        else:
            unassigned_packages.append(package)

    # Handle grouped packages
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

    # Handle deadline packages
    for package in deadline_packages:
        distances = [sum(get_distance(package.address, p.address) for p in truck.packages) for truck in trucks[:2]]
        if not distances[0] and not distances[1]:
            trucks[0].load_package(package)
        elif distances[0] <= distances[1]:
            trucks[0].load_package(package)
        else:
            trucks[1].load_package(package)

    # Handle remaining packages
    for package in unassigned_packages:
        distances = [sum(get_distance(package.address, p.address) for p in truck.packages) for truck in trucks]
        min_distance_index = distances.index(min(distances))
        if len(trucks[min_distance_index].packages) < trucks[min_distance_index].capacity:
            trucks[min_distance_index].load_package(package)
        else:
            for i in range(3):
                if len(trucks[i].packages) < trucks[i].capacity:
                    trucks[i].load_package(package)
                    break

    # Set departure times for trucks
    current_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    
    # First two trucks depart at 8:00 AM
    trucks[0].depart(current_time)
    trucks[1].depart(current_time)

    # Optimize routes and simulate deliveries
    for truck in trucks:
        truck.current_location = "4001 South 700 East, Salt Lake City, UT 84107"
        truck.route = optimize_routes([truck], distance_matrix)[truck.truck_id]
    
    # Simulate deliveries
    active_trucks = trucks[:2]
    while active_trucks:
        for truck in active_trucks[:]:  # Create a copy of the list for iteration
            if not truck.route:
                active_trucks.remove(truck)
                if len(active_trucks) < 2 and trucks[2].packages:
                    trucks[2].time = current_time
                    trucks[2].depart(current_time)
                    active_trucks.append(trucks[2])
                continue

            package, distance = truck.route.pop(0)
            if package:
                current_time = max(current_time, package.load_time or current_time)
                travel_time = distance / truck.speed
                current_time += timedelta(hours=travel_time)
                truck.time = current_time
                truck.deliver_package(package, distance, current_time)
            else:
                travel_time = distance / truck.speed
                current_time += timedelta(hours=travel_time)
                truck.time = current_time
                truck.return_to_hub(distance)

    return package_hash, trucks

def main():
    print("Initializing WGUPS Package Tracking System...")
    package_hash, trucks = initialize_delivery_system()
    print("Initialization complete. Starting interface...")
    
    # Create and run the CLI
    cli = CLI(package_hash, trucks)
    cli.run()

if __name__ == "__main__":
    main()