# WGUPS Routing Program

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

## How to Run This

1. Clone or download the repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Run the program by executing the following command:

   ```bash
   python -m src.main
   ```

The program will simulate the delivery process, log key events, and allow you to query package statuses at different times.
