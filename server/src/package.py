import logging
import re
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, truck_number, delayed, delayed_until, group):
        self.package_id = package_id
        self.address = self.clean_address(address)
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.truck_number = truck_number
        self.delayed = delayed
        self.delayed_until = delayed_until
        self.group = group
        self.status = "At Hub"  # Initial status when the package is created.
        self.delivery_time = None  # Set when the package is delivered.
        self.truck = None  # Tracks which truck the package is on.
        self.load_time = None  # Set when the package is loaded onto a truck.
        self.en_route_time = None  # Set when the truck carrying the package departs
        self.status_history = [("00:00", "At Hub")]  # Updated: Keep track of status changes
        logging.info(f"Initialized Package {self.package_id}")

    def __str__(self):
        return f"Package {self.package_id}: {self.address}, {self.city}, {self.state} {self.zip_code}, Deadline: {self.deadline if self.deadline else 'EOD'}, Weight: {self.weight}kg, Status: {self.status}"

    def load(self, truck_id, time):
        # Update the package status when it is loaded onto a truck.
        self.truck = truck_id
        self.load_time = time
        self.status = "At Hub"
        self.status_history.append((time.strftime("%H:%M"), "At Hub"))
        logging.info(f"Package {self.package_id} loaded onto Truck {truck_id} at {time}")

    def set_en_route(self, time):
        self.en_route_time = time
        self.status = "En Route"
        self.status_history.append((time.strftime("%H:%M"), "En Route"))
        logging.info(f"Package {self.package_id} en route at {time}")

    def deliver(self, time):
        # Mark the package as delivered and set the delivery time.
        self.delivery_time = time
        self.status = "Delivered"
        self.status_history.append((time.strftime("%H:%M"), "Delivered"))
        logging.info(f"Package {self.package_id} delivered at {time}")

    def get_status(self, time):
        # Determine the package status based on the provided time.
        for status_time, status in reversed(self.status_history):
            if datetime.strptime(status_time, "%H:%M").time() <= time.time():
                return status
        return "At Hub"

    @staticmethod
    def clean_address(address):
        # Clean the address by removing parentheses, ZIP codes, and extra characters.
        address = re.sub(r'\(.*?\)', '', address)
        address = re.sub(r'\d{5}', '', address)
        address = re.sub(r'^.*?(?=\d)', '', address, flags=re.DOTALL)
        address = address.replace('\n', ' ').strip()
        return address