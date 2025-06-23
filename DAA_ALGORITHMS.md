# DAA (Design and Analysis of Algorithms) Project
## Bus Seat Allocation Optimizer - Algorithm Implementation

## Overview
This project implements **5 different algorithms** for bus seat allocation, each serving a specific purpose and demonstrating different algorithmic concepts.

---

## 🎯 **Algorithm 1: Greedy Algorithm**

### **Purpose:**
Basic zone-based seat allocation for normal scenarios.

### **Algorithm Type:**
- **Category**: Greedy Approach
- **Time Complexity**: O(n) where n = number of seats
- **Space Complexity**: O(n)

### **How it Works:**
1. Determine destination zone (front/middle/back)
2. Find bus for the time slot
3. Get all booked seats
4. Search for available seat in preferred zone first
5. Fallback to any available seat if preferred zone is full

### **Use Case:**
- Standard bookings without special requirements
- Fast, simple allocation
- Real-time processing

### **Code Implementation:**
```python
def get_available_seat(time_slot, destination):
    # Zone-based greedy allocation
```

---

## 🎯 **Algorithm 2: 0/1 Knapsack Approach**

### **Purpose:**
Optimized seat allocation based on preference scoring.

### **Algorithm Type:**
- **Category**: Optimization Algorithm
- **Time Complexity**: O(n log n) for sorting
- **Space Complexity**: O(n)

### **How it Works:**
1. Calculate preference score for each available seat
2. Sort seats by preference score (descending)
3. Select seat with highest score
4. Update booking status

### **Use Case:**
- Better optimization than greedy
- Considers seat preferences quantitatively
- Still real-time capable

### **Code Implementation:**
```python
def knapsack_seat_allocation(time_slot, destination, student_id):
    # Preference-based optimization
```

---

## 🎯 **Algorithm 3: Priority Queue Algorithm** ⭐ **NEW**

### **Purpose:**
Prioritize students with special needs, injuries, or longer travel distances.

### **Algorithm Type:**
- **Category**: Priority Queue (Heap-based)
- **Time Complexity**: O(n log n) for priority queue operations
- **Space Complexity**: O(n)

### **How it Works:**
1. Calculate priority score based on:
   - Special needs (Injury: +100, Disability: +80, etc.)
   - Travel distance (longer = higher priority)
   - Student ID (tie-breaker)
2. Create priority queue with all pending bookings
3. Allocate seats based on priority order
4. Give special needs students preferred seats (front rows)

### **Priority Scoring System:**
```
Injury: +100 points
Medical Condition: +90 points
Disability: +80 points
Pregnant: +70 points
Elderly: +60 points
Distance: +2 points per KM
```

### **Use Case:**
- Students with injuries or disabilities
- Elderly students
- Pregnant students
- Medical conditions
- Long-distance travelers

### **Code Implementation:**
```python
def priority_queue_seat_allocation(time_slot, destination, student_id, special_needs):
    # Priority-based allocation for special needs
```

---

## 🎯 **Algorithm 4: Round Robin Algorithm** ⭐ **NEW**

### **Purpose:**
Fair seat distribution ensuring equal opportunity for all students.

### **Algorithm Type:**
- **Category**: Scheduling Algorithm
- **Time Complexity**: O(n) for queue operations
- **Space Complexity**: O(n)

### **How it Works:**
1. Sort all bookings by booking time (FIFO)
2. Create round robin queue of available seats
3. Rotate queue based on student's position
4. Allocate next available seat in rotation

### **Use Case:**
- Fair distribution regardless of booking time
- Prevents seat hoarding
- Equal opportunity for all students

### **Code Implementation:**
```python
def round_robin_seat_allocation(time_slot, destination, student_id):
    # Fair distribution using round robin
```

---

## 🎯 **Algorithm 5: Dynamic Programming Knapsack**

### **Purpose:**
Batch optimization for multiple bookings simultaneously.

### **Algorithm Type:**
- **Category**: Dynamic Programming
- **Time Complexity**: O(nW) where n = bookings, W = seats
- **Space Complexity**: O(nW) for DP table

### **How it Works:**
1. Collect all pending bookings for a time slot
2. Create items with values (preference scores) and weights
3. Apply 0/1 Knapsack DP algorithm
4. Allocate seats to maximize total satisfaction

### **Use Case:**
- Batch processing of multiple bookings
- Global optimization
- Not suitable for real-time processing

### **Code Implementation:**
```python
def dynamic_programming_knapsack_seat_allocation(time_slot, destination, student_id):
    # Batch optimization using DP
```

---

## 🔧 **Algorithm Configuration**

### **Switching Between Algorithms:**
Change the `ALLOCATION_ALGORITHM` constant in `app.py`:

```python
ALLOCATION_ALGORITHM = 'greedy'         # Basic zone-based
ALLOCATION_ALGORITHM = 'knapsack'       # Preference-based
ALLOCATION_ALGORITHM = 'priority_queue' # Special needs priority ⭐
ALLOCATION_ALGORITHM = 'round_robin'    # Fair distribution ⭐
ALLOCATION_ALGORITHM = 'dp_knapsack'    # Batch optimization
```

---

## 📊 **Algorithm Comparison**

| Algorithm | Time Complexity | Space Complexity | Optimality | Real-time | Special Features |
|-----------|----------------|------------------|------------|-----------|------------------|
| **Greedy** | O(n) | O(n) | Local optimal | ✅ Yes | Zone-based |
| **Knapsack** | O(n log n) | O(n) | Better than greedy | ✅ Yes | Preference scoring |
| **Priority Queue** | O(n log n) | O(n) | Priority-based | ✅ Yes | Special needs support ⭐ |
| **Round Robin** | O(n) | O(n) | Fair distribution | ✅ Yes | Equal opportunity ⭐ |
| **DP Knapsack** | O(nW) | O(nW) | Global optimal | ❌ No | Batch processing |

---

## 🎓 **DAA Concepts Demonstrated**

### **1. Greedy Algorithm**
- **Concept**: Make locally optimal choice at each step
- **Application**: Zone-based seat allocation
- **Learning**: When to use greedy vs. optimal algorithms

### **2. Dynamic Programming**
- **Concept**: Solve complex problems by breaking into subproblems
- **Application**: Batch seat optimization
- **Learning**: Trade-off between optimality and efficiency

### **3. Priority Queue (Heap)**
- **Concept**: Abstract data type with priority ordering
- **Application**: Special needs student prioritization
- **Learning**: Real-world applications of priority queues

### **4. Round Robin Scheduling**
- **Concept**: Fair distribution algorithm
- **Application**: Equal opportunity seat allocation
- **Learning**: Fairness in resource allocation

### **5. 0/1 Knapsack**
- **Concept**: Optimization with constraints
- **Application**: Preference-based seat allocation
- **Learning**: Constraint satisfaction problems

---

## 🚀 **Real-World Applications**

### **Priority Queue Algorithm:**
- **Healthcare**: Emergency room triage
- **Transportation**: Airport boarding priority
- **Education**: Special needs accommodation
- **Business**: VIP customer service

### **Round Robin Algorithm:**
- **CPU Scheduling**: Process scheduling
- **Load Balancing**: Server request distribution
- **Resource Allocation**: Fair distribution systems
- **Queue Management**: Customer service systems

---

## 📈 **Performance Analysis**

### **Best for Real-time:**
1. **Greedy** - Fastest, simplest
2. **Round Robin** - Fair and fast
3. **Priority Queue** - Balanced performance

### **Best for Optimization:**
1. **DP Knapsack** - Globally optimal
2. **Priority Queue** - Priority-based optimal
3. **Knapsack** - Preference-based optimal

### **Best for Special Cases:**
1. **Priority Queue** - Special needs students
2. **Round Robin** - Fair distribution
3. **Greedy** - Standard cases

---

## 🎯 **Project Highlights**

✅ **5 Different Algorithms** implemented
✅ **Real-world applications** demonstrated
✅ **Special needs support** with priority queue
✅ **Fair distribution** with round robin
✅ **Configurable algorithm** selection
✅ **Comprehensive documentation**
✅ **Performance analysis** provided
✅ **DAA concepts** clearly explained

This project demonstrates a comprehensive understanding of algorithm design and analysis, with practical implementations that solve real-world problems in transportation and resource allocation. 