# Bus Ticket Booking System

A comprehensive Command-Line Interface (CLI) application for managing bus ticket bookings in Bangladesh. This system provides a complete solution for viewing available buses, searching routes, booking tickets, and managing passenger information with persistent data storage.

## 🚌 Features

### Core Functionality

- **View Available Buses**: Display all buses with available seats
- **Search Buses**: Find buses by origin and destination
- **Book Tickets**: Reserve seats with passenger details
- **Ticket Receipts**: Generate formatted ticket confirmations
- **Data Persistence**: Automatic JSON-based data storage
- **Preloaded Schedule**: 11 popular Bangladeshi bus companies with real routes

### Technical Features

- **Type Safety**: Full type hints throughout the codebase
- **Error Handling**: Comprehensive input validation and error messages
- **Case-Insensitive Search**: Flexible bus name and route matching
- **Seat Management**: Automatic seat allocation and refund handling
- **Unique Ticket IDs**: Auto-incrementing ticket identification system

## 📁 Project Structure

```
bus_ticket_booking_system_008011/
├── bus.py                 # Bus class with seat management
├── ticket.py              # Ticket class for booking records
├── user.py                # Admin/User management classes
├── booking_system.py      # Core booking logic and data persistence
├── main.py                # CLI interface and user interaction
├── data_store.json        # Persistent data storage (auto-generated)
└── README.md              # This documentation file
```

## 🏗️ Architecture

### Core Classes

#### `Bus` Class (`bus.py`)

Manages individual bus information and seat operations:

- **Attributes**: name, origin, destination, departure_time, total_seats, price_per_ticket, available_seats
- **Methods**:
  - `get_available_seats()`: Returns current available seats
  - `book_seat(count)`: Decreases available seats, returns success status
  - `refund_seat(count)`: Increases available seats, returns success status
  - `to_dict()` / `from_dict()`: JSON serialization for persistence

#### `Ticket` Class (`ticket.py`)

Represents individual ticket bookings:

- **Attributes**: ticket_id, bus_id, passenger_name, contact_number, bus_name, origin, destination, departure_time, seat_count, price_paid
- **Methods**: `to_dict()` / `from_dict()` for data persistence

#### `User` Classes (`user.py`)

Administrative user management:

- **Admin**: Basic user credentials (username, password)
- **AdminRegistry**: In-memory user storage with signup/login functionality

#### `BookingSystem` Class (`booking_system.py`)

Core business logic and data management:

- **DataStore**: JSON-based persistence layer
- **BookingSystem**: Main booking operations and bus management

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only built-in modules)

### Installation

1. Clone or download the project files
2. Ensure all Python files are in the same directory
3. Run the application:

```bash
python main.py
```

### First Run

On first execution, the system will:

1. Create `data_store.json` for persistent storage
2. Preload 11 Bangladeshi bus companies with sample schedules
3. Initialize the booking system

## 📋 Preloaded Bus Schedule

The system comes with 11 popular Bangladeshi bus companies:

| Bus Company          | Route               | Departure | Price (BDT) | Seats |
| -------------------- | ------------------- | --------- | ----------- | ----- |
| Ena Transport        | Sylhet → Dhaka      | 08:00     | 800         | 40    |
| Hanif Enterprise     | Sylhet → Chittagong | 09:00     | 900         | 40    |
| Shyamoli Paribahan   | Dhaka → Chittagong  | 10:30     | 1000        | 40    |
| Desh Travels         | Dhaka → Sylhet      | 11:00     | 850         | 40    |
| London Express       | Sylhet → Cumilla    | 14:00     | 700         | 40    |
| Saudia Coach         | Sylhet → Feni       | 15:30     | 650         | 40    |
| Green Line Paribahan | Dhaka → Chittagong  | 07:30     | 1200        | 40    |
| Shohagh Paribahan    | Dhaka → Cox's Bazar | 21:00     | 1400        | 40    |
| SilkLine             | Sylhet → Dhaka      | 17:45     | 800         | 40    |
| Unique Paribahan     | Sylhet → Chittagong | 06:30     | 900         | 40    |
| Year-71 Express      | Sylhet → Khulna     | 16:00     | 1300        | 40    |

## 🎯 Usage Guide

### Main Menu Options

```
=== Bus Ticket Booking System ===
1. View Available Buses
2. Search Buses
3. Book Ticket
4. Exit
```

### 1. View Available Buses

Displays all buses with available seats:

```
Available Buses:
- Ena Transport | Sylhet -> Dhaka | 08:00 | 800 BDT | Seats: 40/40
- Hanif Enterprise | Sylhet -> Chittagong | 09:00 | 900 BDT | Seats: 40/40
```

### 2. Search Buses

Search by origin and destination:

```
Enter origin: Sylhet
Enter destination: Dhaka
Matching Buses:
- Ena Transport | Sylhet -> Dhaka | 08:00 | 800 BDT | Seats: 40/40
- SilkLine | Sylhet -> Dhaka | 17:45 | 800 BDT | Seats: 35/40
```

### 3. Book Ticket

Complete booking process:

```
Enter Bus Name: Ena Transport
Enter Passenger Name: John Doe
Enter Contact Number: 01712345678
Enter Seat Count: 2
```

### Ticket Receipt

After successful booking, a formatted receipt is displayed:

```
========== BUS TICKET ==========
Ticket ID     : 1
Passenger     : John Doe
Contact       : 01712345678
Bus           : Ena Transport
Route         : Sylhet -> Dhaka
Departure     : 08:00
Seats         : 2
Amount Paid   : 1600 BDT
================================
```

## 🔧 Technical Details

### Data Persistence

- **File**: `data_store.json`
- **Format**: JSON with buses, tickets, and next_ticket_id
- **Auto-creation**: Generated on first run
- **Encoding**: UTF-8 for proper Bengali text support

### Input Validation

- **Bus Names**: Case-insensitive matching
- **Seat Counts**: Must be positive integers
- **Passenger Info**: Non-empty strings required
- **Price Validation**: Positive values only

### Error Handling

- Invalid bus names
- Insufficient available seats
- Invalid seat counts
- Missing passenger information
- File I/O errors

### Performance Features

- **Efficient Search**: O(n) complexity for bus searches
- **Memory Management**: Automatic garbage collection
- **File Operations**: Minimal I/O with batch updates

## 🛠️ Development

### Code Quality

- **Type Hints**: Full type annotations for all functions
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Graceful error recovery
- **Clean Code**: Follows Python PEP 8 style guidelines

### Extensibility

The modular design allows easy extension:

- Add new bus companies
- Implement additional search criteria
- Add payment processing
- Create admin interfaces
- Add reporting features

### Testing

To test the system:

1. Run `python main.py`
2. Try different search combinations
3. Book multiple tickets
4. Verify seat availability updates
5. Check data persistence in `data_store.json`

## 🔄 Data Management

### Resetting Data

To reset to initial state:

1. Delete `data_store.json`
2. Restart the application
3. System will recreate with preloaded buses

### Data Backup

The `data_store.json` file contains all system data:

- Bus schedules and availability
- All ticket bookings
- Next ticket ID counter

## 🚨 Troubleshooting

### Common Issues

1. **"Bus not found"**: Check bus name spelling (case-insensitive)
2. **"Insufficient seats"**: Try fewer seats or different bus
3. **File errors**: Ensure write permissions in directory
4. **Import errors**: Verify all Python files are present

### System Requirements

- **OS**: Windows, macOS, Linux
- **Python**: 3.7+ (tested on 3.7, 3.8, 3.9, 3.10, 3.11)
- **Memory**: Minimal (uses JSON storage)
- **Disk**: ~10KB for data storage

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please ensure:

- Code follows existing style guidelines
- Type hints are maintained
- Error handling is comprehensive
- Documentation is updated

## 📞 Support

For issues or questions:

1. Check the troubleshooting section
2. Verify Python version compatibility
3. Ensure all files are present
4. Check file permissions

---

**Built with ❤️ for Bangladesh's bus transportation system**
