from datetime import datetime, timedelta

class Truck:
    def __init__(self, truck_id, capacity=16, speed=18):
        self.truck_id = truck_id
        self.capacity = capacity
        self.speed = speed  # miles per hour
        self.packages = []
        self.mileage = 0
        self.current_location = "HUB"
        self.time = datetime.strptime("8:00 AM", "%I:%M %p")

    def load_package(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)
            package.truck = self.truck_id
            return True
        return False

    def deliver_package(self, package, distance):
        travel_time = distance / self.speed
        self.time += timedelta(hours=travel_time)
        self.mileage += distance
        self.current_location = package.address
        package.update_status("Delivered", self.time)
        self.packages.remove(package)

    def return_to_hub(self, distance_to_hub):
        travel_time = distance_to_hub / self.speed
        self.time += timedelta(hours=travel_time)
        self.mileage += distance_to_hub
        self.current_location = "HUB"

    def __str__(self):
        return f"Truck {self.truck_id}: {len(self.packages)}/{self.capacity} packages, {self.mileage:.1f} miles traveled"