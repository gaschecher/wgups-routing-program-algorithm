import csv
from datetime import datetime

def load_distance_data(filename):
    distances = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)[2:]  # Skip the first two columns
        for row in reader:
            if row[0] == "":
                continue
            from_address = row[1]
            distances[from_address] = {headers[i]: float(dist) if dist else 0 for i, dist in enumerate(row[2:]) if dist}
    return distances

def nearest_neighbor(truck, undelivered_packages, distances):
    if not undelivered_packages:
        return None
    
    nearest_package = min(undelivered_packages, key=lambda p: distances[truck.current_location][p.address])
    return nearest_package

def calculate_route(truck, packages, distances):
    undelivered = packages.copy()
    route = []
    
    while undelivered:
        next_package = nearest_neighbor(truck, undelivered, distances)
        if next_package is None:
            break
        
        distance = distances[truck.current_location][next_package.address]
        truck.deliver_package(next_package, distance)
        route.append((next_package, distance))
        undelivered.remove(next_package)
    
    # Return to hub
    distance_to_hub = distances[truck.current_location]["HUB"]
    truck.return_to_hub(distance_to_hub)
    route.append((None, distance_to_hub))
    
    return route

def optimize_routes(trucks, packages, distances):
    # Simple package distribution among trucks
    for i, package in enumerate(packages):
        trucks[i % len(trucks)].load_package(package)
    
    routes = {}
    for truck in trucks:
        routes[truck.truck_id] = calculate_route(truck, truck.packages, distances)
    
    return routes