# Bus Seat Allocation Optimizer

A smart bus seat allocation system that uses advanced algorithms (Greedy and 0/1 Knapsack) to optimize student transportation based on distance and preferences.

## 🚀 Features

- **Smart Seat Allocation**: Uses Greedy and Knapsack algorithms for optimal seat distribution
- **Zone-Based Allocation**: Shorter distances get front seats, longer distances get back seats
- **Real-time Dashboard**: Live monitoring of bus occupancy and seat status
- **Time Slot Management**: Efficient bus reuse between different time slots
- **Modern UI**: Beautiful, responsive interface with animations and particles
- **CSV Data Storage**: Simple file-based storage without database complexity

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python Flask
- **Algorithms**: Greedy Algorithm, 0/1 Knapsack
- **Data Storage**: CSV files
- **Libraries**: AOS (Animate On Scroll), Particles.js, FontAwesome

## 📁 Project Structure

```
bus-seat-allocator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── index.html        # Landing page
│   ├── student.html      # Student booking page
│   └── admin.html        # Admin dashboard
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Shared styles
│   └── js/
│       └── main.js       # Shared JavaScript
└── data/                 # CSV data files (auto-generated)
    ├── routes.csv        # Bus routes and zones
    ├── booking.csv       # All bookings
    └── buses.csv         # Bus information
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd bus-seat-allocator
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 📖 Usage Guide

### For Students

1. **Access Student Portal**
   - Go to the landing page
   - Click "Book Now" or navigate to `/student`

2. **Book Your Seat**
   - Fill in your details (Name, Student ID, Email)
   - Select your preferred time slot (11AM, 1PM, 4PM, 6PM)
   - Choose your destination from the dropdown
   - Click "Book My Seat"

3. **Confirmation**
   - You'll receive a confirmation with your allocated bus and seat number
   - The system automatically assigns seats based on distance and availability

### For Administrators

1. **Access Admin Dashboard**
   - Go to the landing page
   - Click "Admin Login" or navigate to `/admin`
   - Use any credentials (demo mode)

2. **Monitor Bookings**
   - View all current bookings in the table
   - See real-time bus occupancy statistics
   - Monitor seat allocation across all buses

3. **Visual Bus Layout**
   - See a visual representation of each bus
   - Green seats = Available, Red seats = Booked
   - Hover over seats to see booking details

## 🧠 Algorithm Details

### Seat Allocation Logic

The system uses a combination of algorithms for optimal seat allocation:

1. **Zone-Based Allocation**:
   - Front Zone (Rows A-C): Short distance destinations
   - Middle Zone (Rows D-G): Medium distance destinations  
   - Back Zone (Rows H-J): Long distance destinations

2. **Greedy Algorithm**:
   - Prioritizes earlier bookings
   - Assigns seats in preferred zones first
   - Falls back to available seats if preferred zone is full

3. **Bus Reuse Strategy**:
   - Buses can be reused between time slots
   - Optimizes resource utilization
   - Reduces operational costs

### Constants

```python
TOTAL_SEATS = 40  # 10 rows (A–J), 4 seats per row
SEAT_ROWS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
SEAT_COLS = [1, 2, 3, 4]
SEAT_ZONES = {
    'front': ['A', 'B', 'C'],
    'middle': ['D', 'E', 'F', 'G'],
    'back': ['H', 'I', 'J']
}
```

## 📊 Data Format

### Routes (routes.csv)
```csv
Destination,DistanceFromCollege,SeatZone
Rajpur Road,3,front
ISBT,7,middle
Clement Town,12,back
```

### Bookings (booking.csv)
```csv
BookingID,StudentID,Name,Email,BusNumber,SeatNumber,TimeSlot,Destination,BookingDate,Status
1,STU001,John Doe,john@email.com,BUS1,A1,11AM,Rajpur Road,2024-01-15 10:30:00,Confirmed
```

### Buses (buses.csv)
```csv
BusID,BusNumber,TimeSlot,TotalSeats,BookedSeats,AvailableSeats,IsReused,ReusedFrom
B1,BUS1,11AM,40,5,35,False,
```

## 🔧 API Endpoints

- `GET /` - Landing page
- `GET /student` - Student booking page
- `GET /admin` - Admin dashboard
- `GET /api/routes` - Get all routes
- `GET /api/bookings` - Get all bookings
- `GET /api/buses` - Get bus information
- `POST /api/book` - Book a seat

## 🎨 UI Features

- **Particles.js Background**: Animated particle effects on landing page
- **AOS Animations**: Smooth scroll animations throughout the app
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Modern Color Scheme**: Purple gradient theme with clean typography
- **Interactive Elements**: Hover effects, loading states, and smooth transitions

## 🔒 Demo Access

This is a prototype system with demo access:
- **Student Login**: Use any credentials to access student portal
- **Admin Login**: Use any credentials to access admin dashboard
- **No Authentication**: All features are accessible for demonstration

## 🚀 Future Enhancements

- User authentication and authorization
- Database integration (PostgreSQL/MySQL)
- Real-time notifications
- Mobile app development
- Advanced analytics and reporting
- Integration with payment gateways
- Driver and route management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

For questions or support, please open an issue in the repository or contact the development team.

---

**Built with ❤️ for efficient student transportation** 