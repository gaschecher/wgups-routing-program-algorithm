# WGUPS Package Delivery Tracking System

A delivery management system built with Flask (backend) and React (frontend) that optimizes package delivery routes using the Nearest Neighbor algorithm. The system implements a greedy approach where each truck delivers to the closest destination first, while accounting for special constraints like delivery deadlines, package groups, and delayed deliveries. The algorithm achieves efficient routing by:

1. Prioritizing packages with deadlines
2. Finding the shortest path to the next delivery location
3. Minimizing total distance traveled
4. Dynamically adjusting routes based on truck capacity and driver availability
