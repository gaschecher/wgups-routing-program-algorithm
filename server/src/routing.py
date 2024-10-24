from datetime import datetime
import logging
import re
import sys
from .data.locations import location_to_address, distance_matrix

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Clean the address by removing extraneous elements like parentheses, ZIP codes, and directional prefixes.
# This function exists in package.py and routing.py with slight variations. In a production environment, I would move this to a shared folder and reuse the same function.
def clean_address(address):
    if address.upper() == "HUB":
        return "HUB"
    address = re.sub(r'\(.*?\)', '', address)
    address = re.sub(r'\d{5}', '', address)
    address = re.sub(r'^(South|North|East|West|S|N|E|W)\s+', '', address, flags=re.IGNORECASE)
    address = re.sub(r'^.*?(?=\d)', '', address, flags=re.DOTALL)
    address = address.replace('\n', ' ').strip()
    return address

# Get the index of a location from the address, matching cleaned addresses.
def get_location_index(address):
    if address.upper() == "HUB":
        return list(location_to_address.keys()).index("HUB")
    cleaned_address = clean_address(address)
    for index, (location, full_address) in enumerate(location_to_address.items()):
        if cleaned_address in clean_address(full_address) or clean_address(full_address) in cleaned_address:
            return index
    logging.error(f"Address not found: {address}")
    return -1

# Get the distance between two addresses using the distance matrix.
def get_distance(from_address, to_address):
    from_index = get_location_index(from_address)
    to_index = get_location_index(to_address)
    
    if from_index == -1:
        raise ValueError(f"Could not find location index for address: {from_address}")
    if to_index == -1:
        raise ValueError(f"Could not find location index for address: {to_address}")
    
    return distance_matrix[from_index][to_index]

# Find the nearest package for the truck from the list of undelivered packages.
def nearest_neighbor(truck, undelivered_packages):
    logging.debug(f"Finding nearest neighbor for truck {truck.truck_id}")
    if not undelivered_packages:
        logging.debug("No undelivered packages left")
        return None
    
    # Prioritize packages with a deadline.
    deadline_packages = [p for p in undelivered_packages if p.deadline and p.deadline != ""]
    if deadline_packages:
        nearest_package = min(deadline_packages, 
                              key=lambda p: get_distance(truck.current_location, p.address))
    else:
        nearest_package = min(undelivered_packages, 
                              key=lambda p: get_distance(truck.current_location, p.address))
    
    logging.debug(f"Nearest package found: {nearest_package.package_id}")
    return nearest_package

# Calculate the delivery route for a truck using the nearest neighbor.
def calculate_route(truck, packages):
    logging.info(f"Calculating route for truck {truck.truck_id}")
    undelivered = packages.copy()
    route = []
    current_location = "4001 South 700 East, Salt Lake City, UT 84107"  # Packages always start at the HUB.
    
    # Loop through all undelivered packages and build the route.
    while undelivered:
        next_package = nearest_neighbor(truck, undelivered)
        if next_package is None:
            break
        
        try:
            # Calculate the distance to the next package and add it to the route.
            distance = get_distance(current_location, next_package.address)
            route.append((next_package, distance))
            logging.debug(f"Added to route: Package {next_package.package_id}, Distance: {distance}")
            current_location = next_package.address
            undelivered.remove(next_package)
        except ValueError as e:
            logging.error(f"Error calculating distance: {e}")
            logging.error(f"Current location: {current_location}")
            logging.error(f"Next package address: {next_package.address}")
            logging.error(f"Truck ID: {truck.truck_id}")
            logging.error(f"Remaining undelivered packages: {[p.package_id for p in undelivered]}")
            sys.exit(1)
    
    # After all packages are delivered, calculate distance back to the hub.
    try:
        distance_to_hub = get_distance(current_location, "4001 South 700 East, Salt Lake City, UT 84107")
        route.append((None, distance_to_hub))
        logging.debug(f"Added return to hub: Distance: {distance_to_hub}")
    except ValueError as e:
        logging.error(f"Error calculating distance back to hub: {e}")
        logging.error(f"Last location: {current_location}")
        sys.exit(1)
    
    logging.info(f"Finished calculating route for truck {truck.truck_id}. Total stops: {len(route)}")
    return route

# Optimize routes for all trucks.
def optimize_routes(trucks, distances):
    logging.info("Optimizing routes for all trucks")
    routes = {}
    for truck in trucks:
        routes[truck.truck_id] = calculate_route(truck, truck.packages)
    logging.info("Finished optimizing routes")
    return routes