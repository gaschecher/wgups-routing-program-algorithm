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
        self.status = "At Hub"
        self.delivery_time = None
        self.truck = None
        self.load_time = None
        logging.info(f"Initialized Package {self.package_id}")

    def __str__(self):
        return f"Package {self.package_id}: {self.address}, {self.city}, {self.state} {self.zip_code}, Deadline: {self.deadline if self.deadline else 'EOD'}, Weight: {self.weight}kg, Status: {self.status}"

    def load(self, truck_id, time):
        self.truck = truck_id
        self.load_time = time
        self.status = "En Route"
        logging.info(f"Package {self.package_id} loaded onto Truck {truck_id} at {time}")

    def deliver(self, time):
        self.delivery_time = time
        self.status = "Delivered"
        logging.info(f"Package {self.package_id} delivered at {time}")

    def get_status(self, time):
        if self.delivery_time and time >= self.delivery_time:
            status = "Delivered"
        elif self.load_time and time >= self.load_time:
            status = "En Route"
        else:
            status = "At Hub"
        logging.debug(f"Package {self.package_id} status at {time}: {status}")
        return status

    @staticmethod
    def clean_address(address):
        address = re.sub(r'\(.*?\)', '', address)
        address = re.sub(r'\d{5}', '', address)
        address = re.sub(r'^.*?(?=\d)', '', address, flags=re.DOTALL)
        address = address.replace('\n', ' ').strip()
        return address