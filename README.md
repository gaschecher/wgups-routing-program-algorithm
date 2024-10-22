# WGUPS Package Delivery Tracking System

A delivery management system built with Flask (backend) and React (frontend) that optimizes package delivery routes using the Nearest Neighbor algorithm. The system implements a greedy approach where each truck delivers to the closest destination first, while accounting for special constraints like delivery deadlines, package groups, and delayed deliveries. The algorithm achieves efficient routing by:

1. Prioritizing packages with deadlines
2. Finding the shortest path to the next delivery location
3. Minimizing total distance traveled
4. Dynamically adjusting routes based on truck capacity and driver availability

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- Node.js 14.x or higher
- npm (Node Package Manager)
- Git

## Backend Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd delivery-tracking
```

2. Create and activate a Python virtual environment:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

4. Run the Flask server (either method works):

```bash
# Method 1: Direct Python execution
python app.py

# Method 2: Using Flask CLI
# Windows
set FLASK_APP=app
set FLASK_ENV=development
flask run

# macOS/Linux
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

The backend server will start running on `http://localhost:5000`

## Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install Node.js dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

The frontend application will start running on `http://localhost:3000`

## API Endpoints

### Package Routes

- `GET /api/package/<package_id>` - Get details for a specific package
- `GET /api/packages` - Get all packages status
- `GET /api/mileage` - Get total mileage for all trucks
- `GET /api/truck-packages` - Get package status history for all trucks

Query Parameters:

- `time`: Time to check status (HH:MM format)
- `start_time`: Range start time (HH:MM format)
- `end_time`: Range end time (HH:MM format)
