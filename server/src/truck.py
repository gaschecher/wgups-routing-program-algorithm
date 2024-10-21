from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Truck:
    def __init__(self, truck_id, capacity=16, speed=18):
        # Initialize truck attributes
        self.truck_id = truck_id
        self.capacity = capacity
        self.speed = speed
        self.packages = []
        self.mileage = 0
        self.current_location = "4001 South 700 East, Salt Lake City, UT 84107" 
        self.time = datetime.strptime("8:00 AM", "%I:%M %p")
        self.route = []
        logging.info(f"Initialized Truck {self.truck_id}")

    # Load a package onto the truck.
    def load_package(self, package, load_time=None):
        if len(self.packages) < self.capacity:
            self.packages.append(package)
            if load_time:
                package.load(self.truck_id, load_time)
                logging.debug(f"Loaded package {package.package_id} onto Truck {self.truck_id} with delayed load time {load_time}")
            else:
                package.load(self.truck_id, self.time)
                logging.debug(f"Loaded package {package.package_id} onto Truck {self.truck_id}")
            return True
        logging.warning(f"Failed to load package {package.package_id} onto Truck {self.truck_id}: Capacity full")
        return False

    # Deliver a package and update the truck's status.
    def deliver_package(self, package, distance):
        # Calculate travel time based on the distance and truck's speed.
        travel_time = distance / self.speed
        self.time += timedelta(hours=travel_time)  # Update the truck's time after travel.
        self.mileage += distance  # Increase the truck's mileage.
        self.current_location = package.address  # Update the truck's current location.
        package.deliver(self.time)  # Mark the package as delivered at the current time.
        if package in self.packages:
            self.packages.remove(package)  # Remove the package from the truck.
        logging.info(f"Delivered package {package.package_id} at {self.time}. New location: {self.current_location}, New mileage: {self.mileage}")

    # Return the truck to the HUB and update the truck's mileage and time.
    def return_to_hub(self, distance_to_hub):
        travel_time = distance_to_hub / self.speed
        self.time += timedelta(hours=travel_time)  # Update the truck's time after returning.
        self.mileage += distance_to_hub  # Add the distance to the hub to the truck's mileage.
        self.current_location = "4001 South 700 East, Salt Lake City, UT 84107"  # Set current location back to the hub.
        logging.info(f"Truck {self.truck_id} returned to HUB at {self.time}. Total mileage: {self.mileage}")

    def __str__(self):
        return f"Truck {self.truck_id}: {len(self.packages)}/{self.capacity} packages, {self.mileage:.1f} miles traveled"
