from datetime import datetime
import logging
import re
import sys
from data.locations import location_to_address, distance_matrix

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

def optimize_routes(trucks, distance_matrix):
    # Optimize delivery routes for all trucks while minimizing total distance.
    # Returns a dictionary mapping truck IDs to their optimized routes.
    routes = {}
    HUB_ADDRESS = "4001 South 700 East"

    def find_nearest_package(current_location, packages):
        #Find the nearest package from the current location.
        if not packages:
            return None
        return min(packages, key=lambda p: get_distance(current_location, p.address))

    def build_route(truck):
        # Build an optimized route for a single truck.
        route = []
        current_location = HUB_ADDRESS
        remaining_packages = truck.packages.copy()
        
        # First handle deadline packages.
        deadline_packages = sorted(
            [p for p in remaining_packages if p.deadline and p.deadline != ""],
            key=lambda x: (x.deadline, get_distance(current_location, x.address))
        )
        
        # Process deadline packages first.
        for package in deadline_packages:
            if package in remaining_packages:  # Check if package is still unassigned.
                distance = get_distance(current_location, package.address)
                route.append((package, distance))
                current_location = package.address
                remaining_packages.remove(package)
        
        # Process remaining packages using nearest neighbor.
        while remaining_packages:
            next_package = find_nearest_package(current_location, remaining_packages)
            if not next_package:
                break
                
            distance = get_distance(current_location, next_package.address)
            route.append((next_package, distance))
            current_location = next_package.address
            remaining_packages.remove(next_package)
        
        # Add return to hub.
        if route:
            final_distance = get_distance(current_location, HUB_ADDRESS)
            route.append((None, final_distance))
        
        return route

    # Process each truck.
    total_distance = 0
    for truck in trucks:
        route = build_route(truck)
        routes[truck.truck_id] = route
        
        # Calculate and log route distance.
        route_distance = sum(distance for _, distance in route)
        total_distance += route_distance
        logging.info(f"Route {truck.truck_id} distance: {route_distance:.1f} miles")
    
    logging.info(f"Total distance for all routes: {total_distance:.1f} miles")
    return routes