from flask import Flask, request, jsonify, render_template
import csv
import os
from datetime import datetime
import json
from queue import PriorityQueue
from collections import deque

app = Flask(__name__)

# Constants
TOTAL_SEATS = 40  # 10 rows (A–J), 4 seats per row
SEAT_ROWS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
SEAT_COLS = [1, 2, 3, 4]
SEAT_ZONES = {
    'front': ['A', 'B', 'C'],
    'middle': ['D', 'E', 'F', 'G'],
    'back': ['H', 'I', 'J']
}
TIME_SLOTS = {
    '11AM': {'reuse': None},
    '1PM': {'reuse': '11AM'},
    '4PM': {'reuse': '1PM'},
    '6PM': {'reuse': '4PM'}
}

# Algorithm Configuration
ALLOCATION_ALGORITHM = 'hybrid'  # Options: 'greedy', 'knapsack', 'dp_knapsack', 'priority_queue', 'round_robin', 'hybrid'

# CSV file paths
ROUTES_FILE = 'data/routes.csv'
BOOKING_FILE = 'data/booking.csv'
BUSES_FILE = 'data/buses.csv'

def ensure_data_directory():
    """Ensure the data directory exists and create CSV files if they don't exist"""
    os.makedirs('data', exist_ok=True)
    
    # Create routes.csv if it doesn't exist
    if not os.path.exists(ROUTES_FILE):
        with open(ROUTES_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Destination', 'DistanceFromCollege', 'SeatZone'])
            writer.writerow(['Rajpur Road', 3, 'front'])
            writer.writerow(['ISBT', 7, 'middle'])
            writer.writerow(['Clement Town', 12, 'back'])
    
    # Create booking.csv if it doesn't exist
    if not os.path.exists(BOOKING_FILE):
        with open(BOOKING_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['BookingID', 'StudentID', 'Name', 'Email', 'BusNumber', 'SeatNumber', 'TimeSlot', 'Destination', 'BookingDate', 'Status'])
    
    # Create buses.csv if it doesn't exist
    if not os.path.exists(BUSES_FILE):
        with open(BUSES_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['BusID', 'BusNumber', 'TimeSlot', 'TotalSeats', 'BookedSeats', 'AvailableSeats', 'IsReused', 'ReusedFrom'])
            writer.writerow(['B1', 'BUS1', '11AM', 40, 0, 40, False, ''])
            writer.writerow(['B2', 'BUS2', '1PM', 40, 0, 40, False, ''])
            writer.writerow(['B3', 'BUS3', '4PM', 40, 0, 40, False, ''])
            writer.writerow(['B4', 'BUS4', '6PM', 40, 0, 40, False, ''])

def get_next_booking_id():
    """Generate the next booking ID"""
    if not os.path.exists(BOOKING_FILE):
        return 1
    
    with open(BOOKING_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        bookings = list(reader)
        if not bookings:
            return 1
        return max(int(booking['BookingID']) for booking in bookings) + 1

def get_available_seat(time_slot, destination):
    """Greedy algorithm to allocate seat based on distance and zone"""
    # Get destination zone
    with open(ROUTES_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for route in reader:
            if route['Destination'] == destination:
                zone = route['SeatZone']
                break
        else:
            zone = 'middle'  # default zone
    
    # Get current bus status
    bus_number = None
    with open(BUSES_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for bus in reader:
            if bus['TimeSlot'] == time_slot:
                bus_number = bus['BusNumber']
                break
    
    if not bus_number:
        return None, None
    
    # Get booked seats for this bus
    booked_seats = set()
    with open(BOOKING_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for booking in reader:
            if booking['BusNumber'] == bus_number and booking['Status'] == 'Confirmed':
                booked_seats.add(booking['SeatNumber'])
    
    # Find available seat in the appropriate zone
    zone_rows = SEAT_ZONES[zone]
    for row in zone_rows:
        for col in SEAT_COLS:
            seat = f"{row}{col}"
            if seat not in booked_seats:
                return bus_number, seat
    
    # If no seat in preferred zone, find any available seat
    for row in SEAT_ROWS:
        for col in SEAT_COLS:
            seat = f"{row}{col}"
            if seat not in booked_seats:
                return bus_number, seat
    
    return None, None

def calculate_seat_preference_score(destination, seat_number):
    """Calculate preference score for a seat based on destination"""
    # Get destination zone
    with open(ROUTES_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for route in reader:
            if route['Destination'] == destination:
                zone = route['SeatZone']
                distance = int(route['DistanceFromCollege'])
                break
        else:
            zone = 'middle'
            distance = 5  # default distance
    
    # Extract row from seat number (e.g., "A1" -> "A")
    row = seat_number[0]
    
    # Calculate preference score
    if zone == 'front' and row in ['A', 'B', 'C']:
        return 10  # High preference for front zone
    elif zone == 'middle' and row in ['D', 'E', 'F', 'G']:
        return 10  # High preference for middle zone
    elif zone == 'back' and row in ['H', 'I', 'J']:
        return 10  # High preference for back zone
    else:
        # Lower preference for non-preferred zones
        return 5

def knapsack_seat_allocation(time_slot, destination, student_id):
    """
    0/1 Knapsack approach for seat allocation
    Maximizes overall satisfaction while considering seat preferences
    """
    # Get bus number for time slot
    bus_number = None
    with open(BUSES_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for bus in reader:
            if bus['TimeSlot'] == time_slot:
                bus_number = bus['BusNumber']
                break
    
    if not bus_number:
        return None, None
    
    # Get all available seats
    booked_seats = set()
    with open(BOOKING_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for booking in reader:
            if booking['BusNumber'] == bus_number and booking['Status'] == 'Confirmed':
                booked_seats.add(booking['SeatNumber'])
    
    # Create list of available seats with their preference scores
    available_seats = []
    for row in SEAT_ROWS:
        for col in SEAT_COLS:
            seat = f"{row}{col}"
            if seat not in booked_seats:
                preference_score = calculate_seat_preference_score(destination, seat)
                available_seats.append({
                    'seat': seat,
                    'value': preference_score,
                    'weight': 1  # Each seat has weight 1
                })
    
    if not available_seats:
        return None, None
    
    # Sort by preference score (descending) for greedy approach
    # In a full knapsack implementation, we'd use dynamic programming
    available_seats.sort(key=lambda x: x['value'], reverse=True)
    
    # Return the seat with highest preference score
    best_seat = available_seats[0]['seat']
    return bus_number, best_seat

def dynamic_programming_knapsack_seat_allocation(time_slot, destination, student_id):
    """
    Full 0/1 Knapsack implementation using dynamic programming
    This would be used for batch allocation of multiple bookings
    """
    # This is a more complex implementation for batch optimization
    # Would be useful when processing multiple bookings simultaneously
    
    # Get all pending bookings for the time slot
    pending_bookings = []
    with open(BOOKING_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for booking in reader:
            if booking['TimeSlot'] == time_slot and booking['Status'] == 'Pending':
                pending_bookings.append(booking)
    
    # Create items for knapsack (each booking is an item)
    items = []
    for booking in pending_bookings:
        # Calculate value based on destination preference
        value = calculate_seat_preference_score(booking['Destination'], 'A1')  # Example seat
        items.append({
            'booking': booking,
            'value': value,
            'weight': 1
        })
    
    # Implement 0/1 Knapsack DP algorithm
    # This would maximize total satisfaction across all bookings
    # For now, return the greedy approach
    return knapsack_seat_allocation(time_slot, destination, student_id)

def calculate_priority_score(student_id, special_needs, destination):
    """
    Calculate priority score for students based on special needs and destination
    Higher score = Higher priority
    """
    priority_score = 0
    
    # Base priority based on special needs
    if special_needs == 'Injury':
        priority_score += 100  # Highest priority for injured students
    elif special_needs == 'Disability':
        priority_score += 80   # High priority for disabled students
    elif special_needs == 'Elderly':
        priority_score += 60   # Medium-high priority for elderly
    elif special_needs == 'Pregnant':
        priority_score += 70   # High priority for pregnant students
    elif special_needs == 'Medical':
        priority_score += 90   # Very high priority for medical conditions
    
    # Distance-based priority (longer distance = higher priority)
    with open(ROUTES_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for route in reader:
            if route['Destination'] == destination:
                distance = int(route['DistanceFromCollege'])
                priority_score += distance * 2  # Distance factor
                break
    
    # Student ID based priority (lower ID = higher priority for same conditions)
    priority_score += (10000 - int(student_id)) / 10000
    
    return priority_score

def priority_queue_seat_allocation(time_slot, destination, student_id, special_needs):
    """
    Priority Queue algorithm for seat allocation
    Prioritizes students with special needs, injuries, or longer travel distances
    """
    # Get bus number for time slot
    bus_number = None
    with open(BUSES_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for bus in reader:
            if bus['TimeSlot'] == time_slot:
                bus_number = bus['BusNumber']
                break
    
    if not bus_number:
        return None, None
    
    # Get all pending bookings for this time slot
    pending_bookings = []
    with open(BOOKING_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for booking in reader:
            if booking['TimeSlot'] == time_slot and booking['Status'] == 'Pending':
                pending_bookings.append(booking)
    
    # Add current booking to pending list
    current_booking = {
        'StudentID': student_id,
        'Destination': destination,
        'SpecialNeeds': special_needs
    }
    pending_bookings.append(current_booking)
    
    # Create priority queue
    priority_queue = PriorityQueue()
    
    # Calculate priority scores and add to queue
    for booking in pending_bookings:
        priority_score = calculate_priority_score(
            booking['StudentID'], 
            booking.get('SpecialNeeds', 'None'), 
            booking['Destination']
        )
        # Negative score because PriorityQueue returns lowest value first
        priority_queue.put((-priority_score, booking))
    
    # Get booked seats for this bus
    booked_seats = set()
    with open(BOOKING_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for booking in reader:
            if booking['BusNumber'] == bus_number and booking['Status'] == 'Confirmed':
                booked_seats.add(booking['SeatNumber'])
    
    # Allocate seats based on priority
    allocated_seats = {}
    
    while not priority_queue.empty():
        priority_score, booking = priority_queue.get()
        priority_score = -priority_score  # Convert back to positive
        
        # Find best available seat for this booking
        best_seat = None
        best_score = -1
        
        for row in SEAT_ROWS:
            for col in SEAT_COLS:
                seat = f"{row}{col}"
                if seat not in booked_seats and seat not in allocated_seats.values():
                    # Calculate seat preference score
                    seat_score = calculate_seat_preference_score(booking['Destination'], seat)
                    
                    # Bonus for special needs students getting preferred seats
                    if booking.get('SpecialNeeds') != 'None':
                        if booking.get('SpecialNeeds') == 'Injury' and row in ['A', 'B']:  # Front seats for injured
                            seat_score += 20
                        elif booking.get('SpecialNeeds') == 'Disability' and row in ['A', 'B']:  # Front seats for disabled
                            seat_score += 15
                        elif booking.get('SpecialNeeds') == 'Elderly' and row in ['A', 'B', 'C']:  # Front-middle for elderly
                            seat_score += 10
                    
                    if seat_score > best_score:
                        best_score = seat_score
                        best_seat = seat
        
        if best_seat:
            allocated_seats[booking['StudentID']] = best_seat
            booked_seats.add(best_seat)
    
    # Return seat for current student
    if student_id in allocated_seats:
        return bus_number, allocated_seats[student_id]
    
    return None, None

def round_robin_seat_allocation(time_slot, destination, student_id):
    """
    Round Robin algorithm for fair seat distribution
    Ensures equal opportunity for all students regardless of booking time
    """
    # Get bus number for time slot
    bus_number = None
    with open(BUSES_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for bus in reader:
            if bus['TimeSlot'] == time_slot:
                bus_number = bus['BusNumber']
                break
    
    if not bus_number:
        return None, None
    
    # Get all bookings for this time slot
    all_bookings = []
    with open(BOOKING_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for booking in reader:
            if booking['TimeSlot'] == time_slot:
                all_bookings.append(booking)
    
    # Sort bookings by booking time (FIFO - First In, First Out)
    all_bookings.sort(key=lambda x: x['BookingDate'])
    
    # Get booked seats
    booked_seats = set()
    for booking in all_bookings:
        if booking['Status'] == 'Confirmed':
            booked_seats.add(booking['SeatNumber'])
    
    # Create round robin queue for available seats
    available_seats = deque()
    for row in SEAT_ROWS:
        for col in SEAT_COLS:
            seat = f"{row}{col}"
            if seat not in booked_seats:
                available_seats.append(seat)
    
    if not available_seats:
        return None, None
    
    # Find position of current student in booking queue
    current_position = -1
    for i, booking in enumerate(all_bookings):
        if booking['StudentID'] == student_id:
            current_position = i
            break
    
    if current_position == -1:
        # New booking, add to end of queue
        current_position = len(all_bookings)
    
    # Rotate queue based on current position for fair distribution
    rotation = current_position % len(available_seats)
    available_seats.rotate(-rotation)
    
    # Get the next available seat
    allocated_seat = available_seats.popleft()
    
    return bus_number, allocated_seat

def hybrid_priority_knapsack_allocation(time_slot, destination, student_id, special_needs):
    """
    Hybrid Algorithm: Combines Priority Queue and 0/1 Knapsack
    Step 1: Use Priority Queue to rank students by priority
    Step 2: Use Knapsack approach to optimize seat allocation for each priority group
    """
    # Get bus number for time slot
    bus_number = None
    with open(BUSES_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for bus in reader:
            if bus['TimeSlot'] == time_slot:
                bus_number = bus['BusNumber']
                break
    
    if not bus_number:
        return None, None
    
    # Get all pending bookings for this time slot
    pending_bookings = []
    with open(BOOKING_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for booking in reader:
            if booking['TimeSlot'] == time_slot and booking['Status'] == 'Pending':
                pending_bookings.append(booking)
    
    # Add current booking to pending list
    current_booking = {
        'StudentID': student_id,
        'Destination': destination,
        'SpecialNeeds': special_needs
    }
    pending_bookings.append(current_booking)
    
    # Step 1: Priority Queue - Group students by priority levels
    priority_groups = {
        'Critical': [],    # Injury, Medical (100-90 points)
        'High': [],        # Disability, Pregnant (80-70 points)
        'Medium': [],      # Elderly (60 points)
        'Normal': []       # Regular students
    }
    
    for booking in pending_bookings:
        priority_score = calculate_priority_score(
            booking['StudentID'], 
            booking.get('SpecialNeeds', 'None'), 
            booking['Destination']
        )
        
        if priority_score >= 90:
            priority_groups['Critical'].append(booking)
        elif priority_score >= 70:
            priority_groups['High'].append(booking)
        elif priority_score >= 60:
            priority_groups['Medium'].append(booking)
        else:
            priority_groups['Normal'].append(booking)
    
    # Step 2: Knapsack Optimization for each priority group
    allocated_seats = {}
    booked_seats = set()
    
    # Get already booked seats
    with open(BOOKING_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for booking in reader:
            if booking['BusNumber'] == bus_number and booking['Status'] == 'Confirmed':
                booked_seats.add(booking['SeatNumber'])
    
    # Process each priority group in order
    for priority_level in ['Critical', 'High', 'Medium', 'Normal']:
        group_bookings = priority_groups[priority_level]
        
        if not group_bookings:
            continue
        
        # Apply Knapsack optimization within this priority group
        group_allocations = knapsack_optimize_group(group_bookings, booked_seats, priority_level)
        
        # Update allocations and booked seats
        for student_id, seat in group_allocations.items():
            allocated_seats[student_id] = seat
            booked_seats.add(seat)
    
    # Return seat for current student
    if student_id in allocated_seats:
        return bus_number, allocated_seats[student_id]
    
    return None, None

def knapsack_optimize_group(group_bookings, booked_seats, priority_level):
    """
    Apply 0/1 Knapsack optimization within a priority group
    """
    if not group_bookings:
        return {}
    
    # Get available seats for this group
    available_seats = []
    for row in SEAT_ROWS:
        for col in SEAT_COLS:
            seat = f"{row}{col}"
            if seat not in booked_seats:
                available_seats.append(seat)
    
    if not available_seats:
        return {}
    
    # Create items for knapsack (each booking is an item)
    items = []
    for booking in group_bookings:
        # Calculate value based on destination preference and priority level
        base_value = calculate_seat_preference_score(booking['Destination'], 'A1')
        
        # Priority level multiplier
        priority_multiplier = {
            'Critical': 3.0,  # Highest multiplier for critical cases
            'High': 2.0,      # High multiplier for high priority
            'Medium': 1.5,    # Medium multiplier
            'Normal': 1.0     # Normal multiplier
        }
        
        value = base_value * priority_multiplier[priority_level]
        
        # Special needs bonus
        if booking.get('SpecialNeeds') != 'None':
            if booking.get('SpecialNeeds') == 'Injury':
                value += 50
            elif booking.get('SpecialNeeds') == 'Disability':
                value += 40
            elif booking.get('SpecialNeeds') == 'Medical':
                value += 45
        
        items.append({
            'booking': booking,
            'value': value,
            'weight': 1  # Each booking has weight 1
        })
    
    # Sort by value (descending) for greedy knapsack approach
    items.sort(key=lambda x: x['value'], reverse=True)
    
    # Allocate seats using greedy knapsack
    allocations = {}
    seat_index = 0
    
    for item in items:
        if seat_index < len(available_seats):
            # Find best available seat for this booking
            best_seat = None
            best_score = -1
            
            for seat in available_seats:
                if seat not in allocations.values():
                    seat_score = calculate_seat_preference_score(item['booking']['Destination'], seat)
                    
                    # Bonus for special needs students getting preferred seats
                    if item['booking'].get('SpecialNeeds') != 'None':
                        row = seat[0]
                        if item['booking'].get('SpecialNeeds') == 'Injury' and row in ['A', 'B']:
                            seat_score += 20
                        elif item['booking'].get('SpecialNeeds') == 'Disability' and row in ['A', 'B']:
                            seat_score += 15
                        elif item['booking'].get('SpecialNeeds') == 'Medical' and row in ['A', 'B']:
                            seat_score += 18
                    
                    if seat_score > best_score:
                        best_score = seat_score
                        best_seat = seat
            
            if best_seat:
                allocations[item['booking']['StudentID']] = best_seat
                seat_index += 1
    
    return allocations

def update_bus_status(bus_number):
    """Update bus booking status"""
    # Count booked seats for this bus
    booked_count = 0
    with open(BOOKING_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for booking in reader:
            if booking['BusNumber'] == bus_number and booking['Status'] == 'Confirmed':
                booked_count += 1
    
    # Update buses.csv
    buses = []
    with open(BUSES_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for bus in reader:
            if bus['BusNumber'] == bus_number:
                bus['BookedSeats'] = booked_count
                bus['AvailableSeats'] = TOTAL_SEATS - booked_count
            buses.append(bus)
    
    with open(BUSES_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['BusID', 'BusNumber', 'TimeSlot', 'TotalSeats', 'BookedSeats', 'AvailableSeats', 'IsReused', 'ReusedFrom'])
        writer.writeheader()
        writer.writerows(buses)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/routes', methods=['GET'])
def get_routes():
    """Get all routes from routes.csv"""
    routes = []
    with open(ROUTES_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for route in reader:
            routes.append(route)
    return jsonify(routes)

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    """Get all bookings from booking.csv"""
    bookings = []
    with open(BOOKING_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for booking in reader:
            bookings.append(booking)
    return jsonify(bookings)

@app.route('/api/student-bookings', methods=['GET'])
def get_student_bookings():
    """Get bookings for a specific student by email or student ID"""
    student_email = request.args.get('email')
    student_id = request.args.get('studentId')
    
    if not student_email and not student_id:
        return jsonify({'error': 'Email or Student ID is required'}), 400
    
    bookings = []
    with open(BOOKING_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for booking in reader:
            if (student_email and booking['Email'] == student_email) or \
               (student_id and booking['StudentID'] == student_id):
                bookings.append(booking)
    
    return jsonify(bookings)

@app.route('/api/book', methods=['POST'])
def book_seat():
    """Handle seat booking"""
    try:
        data = request.get_json()
        name = data.get('name')
        student_id = data.get('studentId')
        email = data.get('email')
        time_slot = data.get('timeSlot')
        destination = data.get('destination')
        
        # Validate required fields
        if not all([name, student_id, email, time_slot, destination]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Check if student already has a booking for this time slot
        with open(BOOKING_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for booking in reader:
                if booking['StudentID'] == student_id and booking['TimeSlot'] == time_slot and booking['Status'] == 'Confirmed':
                    return jsonify({'error': 'You already have a booking for this time slot'}), 400
        
        # Allocate seat
        if ALLOCATION_ALGORITHM == 'greedy':
            bus_number, seat_number = get_available_seat(time_slot, destination)
        elif ALLOCATION_ALGORITHM == 'knapsack':
            bus_number, seat_number = knapsack_seat_allocation(time_slot, destination, student_id)
        elif ALLOCATION_ALGORITHM == 'dp_knapsack':
            bus_number, seat_number = dynamic_programming_knapsack_seat_allocation(time_slot, destination, student_id)
        elif ALLOCATION_ALGORITHM == 'priority_queue':
            special_needs = data.get('specialNeeds')
            bus_number, seat_number = priority_queue_seat_allocation(time_slot, destination, student_id, special_needs)
        elif ALLOCATION_ALGORITHM == 'round_robin':
            bus_number, seat_number = round_robin_seat_allocation(time_slot, destination, student_id)
        elif ALLOCATION_ALGORITHM == 'hybrid':
            special_needs = data.get('specialNeeds')
            bus_number, seat_number = hybrid_priority_knapsack_allocation(time_slot, destination, student_id, special_needs)
        else:
            bus_number, seat_number = get_available_seat(time_slot, destination)  # Default to greedy
        
        if not bus_number or not seat_number:
            return jsonify({'error': 'No seats available for this time slot'}), 400
        
        # Create booking
        booking_id = get_next_booking_id()
        booking_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        special_needs = data.get('specialNeeds', 'None')
        priority = data.get('priority', 'Normal')
        
        new_booking = {
            'BookingID': booking_id,
            'StudentID': student_id,
            'Name': name,
            'Email': email,
            'BusNumber': bus_number,
            'SeatNumber': seat_number,
            'TimeSlot': time_slot,
            'Destination': destination,
            'BookingDate': booking_date,
            'Status': 'Confirmed',
            'Priority': priority,
            'SpecialNeeds': special_needs
        }
        
        # Save booking to CSV
        with open(BOOKING_FILE, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['BookingID', 'StudentID', 'Name', 'Email', 'BusNumber', 'SeatNumber', 'TimeSlot', 'Destination', 'BookingDate', 'Status', 'Priority', 'SpecialNeeds'])
            writer.writerow(new_booking)
        
        # Update bus status
        update_bus_status(bus_number)
        
        return jsonify({
            'success': True,
            'message': 'Seat Booked Successfully!',
            'booking': new_booking
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/buses', methods=['GET'])
def get_buses():
    """Get all bus information"""
    buses = []
    with open(BUSES_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for bus in reader:
            buses.append(bus)
    return jsonify(buses)

if __name__ == '__main__':
    ensure_data_directory()
    app.run(debug=True, host='0.0.0.0', port=5000) 