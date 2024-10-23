# WGUPS Package Delivery Tracking System

A delivery management system built with Python that optimizes package delivery routes using the Nearest Neighbor algorithm. The system implements a greedy approach where each truck delivers to the closest destination first, while accounting for special constraints like delivery deadlines, package groups, and delayed deliveries. The algorithm achieves efficient routing by:

1. Prioritizing packages with deadlines
2. Finding the shortest path to the next delivery location
3. Minimizing total distance traveled
4. Dynamically adjusting routes based on truck capacity and driver availability

## Setup and Installation

1. Clone or download the repository to your local machine
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

## Running the Program

1. Make sure your virtual environment is activated (you should see `(venv)` in your terminal)
2. Run the program in interactive mode:
   ```bash
   python main.py --interactive
   ```
![image](https://github.com/user-attachments/assets/ec1c8df3-0579-4088-999d-aa6da54f0679)


## Program Flow

### 1. Data Initialization
- Creates a custom hash table to store package data
- Initializes truck objects with capacity and speed constraints
- Loads package data including addresses, deadlines, and special requirements

### 2. Package Assignment Process
- Packages are first sorted by constraints (truck requirements, groups, deadlines)
- Priority assignment:
  - Packages with specific truck assignments
  - Grouped packages that must be delivered together
  - Delayed packages assigned to truck 3
  - Packages with deadlines
  - Remaining packages based on optimal routing

### 3. Route Optimization
- Uses nearest neighbor algorithm to determine delivery order
- Considers package deadlines and special requirements
- Calculates optimal routes for each truck

### 4. Delivery Simulation
- Trucks depart hub at 8:00 AM
- Tracks delivery times, mileage, and package status
- Handles delayed packages and special timing requirements
- Updates package status (at hub, en route, delivered)

### 5. User Interface
- Provides interactive menu for package tracking
- Allows status lookup by package ID and time
- Shows delivery status for all packages in a time range
- Reports total mileage for each truck

## Project Structure

### 1. `main.py`
Handles the overall execution of the program, including initializing the system, assigning packages to trucks, simulating deliveries, and allowing user queries.

### 2. `hash_table.py`
Implements a hash table to efficiently store and retrieve package data.

### 3. `package.py`
Defines the `Package` class, which holds package details and tracks its status throughout the delivery process.

### 4. `truck.py`
Defines the `Truck` class, responsible for managing truck operations like loading, delivering packages, and returning to the hub.

### 5. `routing.py`
Contains functions to optimize truck delivery routes and calculate distances between package locations.

### 6. `data/locations.py`
Provides a mapping of location names to addresses and a distance matrix for calculating distances between different addresses.

### 7. `data/packages.py`
Contains the initial package data including addresses, deadlines, and other relevant information for each package.

## Key Features

- Custom hash table implementation for efficient package lookup
- Dynamic route optimization using nearest neighbor algorithm
- Real-time package status tracking
- Support for special delivery requirements:
  - Package deadlines
  - Grouped deliveries
  - Delayed packages
  - Specific truck assignments
- Comprehensive reporting system

## Package Status Definitions

- **At Hub**: Package is at the WGUPS hub awaiting loading
- **En Route**: Package has been loaded and is being delivered
- **Delivered**: Package has been successfully delivered (includes delivery time)
- **Delayed**: Package is delayed and will be available at a specified time

## Troubleshooting

If you encounter any issues:

1. Make sure your virtual environment is activated (you should see `(venv)` in your terminal)
2. Ensure you're in the correct directory containing the `main.py` file
3. Verify that all required files are present in the project structure
