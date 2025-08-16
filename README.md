# Bus Ticket Booking System

A modern **Graphical User Interface (GUI)** desktop application for managing bus ticket bookings in Bangladesh. Built with PyQt6, this system provides an intuitive, Material Design-inspired interface for viewing available buses, searching routes, booking tickets, and managing passenger information with persistent data storage and real-time updates.

## 🚌 Features

### Core Functionality

- **Modern GUI Interface**: Beautiful PyQt6-based desktop application
- **Real-time Updates**: Auto-reload functionality every 5 seconds
- **View Available Buses**: Interactive table display with all bus information
- **Advanced Search**: Find buses by origin and destination with instant results
- **Easy Booking**: Streamlined ticket booking with dropdown selection
- **Ticket Receipts**: Professional receipt dialogs with shadow effects
- **Data Persistence**: Automatic JSON-based data storage
- **Preloaded Schedule**: 24 popular Bangladeshi bus companies with real routes

### Technical Features

- **Type Safety**: Full type hints throughout the codebase
- **Error Handling**: Comprehensive input validation and user-friendly error messages
- **Case-Insensitive Search**: Flexible bus name and route matching
- **Seat Management**: Automatic seat allocation and refund handling
- **Unique Ticket IDs**: Auto-incrementing ticket identification system
- **Material Design**: Modern dark theme with purple accent colors
- **Responsive UI**: Clean, professional interface with hover effects

## 📁 Project Structure

```
bus_ticket_booking_system_008011/
├── bus.py                 # Bus class with seat management
├── ticket.py              # Ticket class for booking records
├── user.py                # Admin/User management classes
├── booking_system.py      # Core booking logic and data persistence
├── main.py                # Application entry point (launches GUI)
├── gui.py                 # PyQt6 GUI implementation
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

#### GUI Components (`gui.py`)

Modern PyQt6-based user interface:

- **MainWindow**: Main application window with tabbed interface
- **AvailableBusesTab**: Table display of all available buses
- **SearchTab**: Route search functionality
- **BookTab**: Ticket booking interface
- **ReceiptDialog**: Professional ticket receipt display

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- PyQt6 library

### Installation

1. **Install PyQt6**:

   ```bash
   pip install PyQt6
   ```

2. **Clone or download** the project files

3. **Run the application**:
   ```bash
   python main.py
   ```

### First Run

On first execution, the system will:

1. Create `data_store.json` for persistent storage
2. Preload 24 Bangladeshi bus companies with sample schedules
3. Launch the modern GUI interface

## 📋 Preloaded Bus Schedule

The system comes with **24 popular Bangladeshi bus companies**:

| Bus Company           | Route                    | Departure | Price (BDT) | Seats |
| --------------------- | ------------------------ | --------- | ----------- | ----- |
| Ena Transport         | Sylhet → Dhaka           | 08:00     | 800         | 40    |
| Hanif Enterprise      | Sylhet → Chittagong      | 09:00     | 900         | 40    |
| Shyamoli Paribahan    | Dhaka → Chittagong       | 10:30     | 1000        | 40    |
| Desh Travels          | Dhaka → Sylhet           | 11:00     | 850         | 40    |
| London Express        | Sylhet → Cumilla         | 14:00     | 700         | 40    |
| Saudia Coach          | Sylhet → Feni            | 15:30     | 650         | 40    |
| Green Line Paribahan  | Dhaka → Chittagong       | 07:30     | 1200        | 40    |
| Shohagh Paribahan     | Dhaka → Cox's Bazar      | 21:00     | 1400        | 40    |
| SilkLine              | Sylhet → Dhaka           | 17:45     | 800         | 40    |
| Unique Paribahan      | Sylhet → Chittagong      | 06:30     | 900         | 40    |
| Year-71 Express       | Sylhet → Khulna          | 16:00     | 1300        | 40    |
| Shyamoli NR Travels   | Sylhet → Jessore         | 20:00     | 1350        | 40    |
| Ena Transport         | Sylhet → Rajshahi        | 07:45     | 1400        | 40    |
| London Express        | Sylhet → Bogra           | 12:30     | 1100        | 40    |
| Hanif Enterprise      | Sylhet → Feni            | 13:45     | 700         | 40    |
| Desh Travels          | Dhaka → Rajshahi         | 09:15     | 1000        | 40    |
| Tungipara Express     | Dhaka → Gopalganj        | 06:45     | 600         | 40    |
| S Alam Paribahan      | Chittagong → Cox's Bazar | 05:30     | 900         | 40    |
| Ena Transport         | Sylhet → Cox's Bazar     | 22:15     | 1700        | 40    |
| Saintmartin Paribahan | Dhaka → Teknaf           | 23:00     | 1800        | 40    |
| Green Line Paribahan  | Sylhet → Dhaka           | 15:00     | 1200        | 40    |
| Shohagh Paribahan     | Sylhet → Dhaka           | 23:45     | 900         | 40    |
| Haque Enterprise      | Sylhet → Moulvibazar     | 10:00     | 400         | 40    |
| NR Travels            | Sylhet → Barisal         | 18:30     | 1200        | 40    |

## 🎯 GUI Usage Guide

### Main Interface

The application features a modern tabbed interface with three main sections:

#### 1. Available Buses Tab

- **Real-time table** showing all buses with available seats
- **Auto-refresh** every 5 seconds
- **Columns**: Bus Name, Route, Departure, Price (BDT), Seats (Available/Total)
- **Interactive**: Click to select rows

#### 2. Search Tab

- **Origin and Destination** input fields
- **Instant search** functionality
- **Results table** with matching buses
- **Case-insensitive** search

#### 3. Book Ticket Tab

- **Dropdown selection** for bus choice
- **Passenger details** input fields
- **Seat count** spinner
- **Professional receipt** dialog after booking

### Booking Process

1. **Select Bus**: Choose from dropdown (shows route and time)
2. **Enter Details**: Passenger name and contact number
3. **Choose Seats**: Select number of seats (1-100)
4. **Book**: Click "Book Ticket" button
5. **Receipt**: View professional ticket receipt

### Ticket Receipt

After successful booking, a beautiful receipt dialog displays:

```
Ticket Receipt
Ticket ID     : 1
Passenger     : John Doe
Contact       : 01712345678
Bus           : Ena Transport
Route         : Sylhet -> Dhaka
Departure     : 08:00
Seats         : 2
Amount Paid   : 1600 BDT
```

## 🔧 Technical Details

### GUI Framework

- **PyQt6**: Modern Python binding for Qt framework
- **Material Design**: Dark theme with purple accent (#6200EE)
- **Responsive Layout**: Adaptive to window resizing
- **Professional Styling**: Rounded corners, shadows, hover effects

### Auto-Reload System

- **5-second intervals**: Automatic data refresh
- **Background updates**: No user intervention required
- **Real-time sync**: Changes appear immediately
- **Efficient**: Minimal performance impact

### Data Persistence

- **File**: `data_store.json`
- **Format**: JSON with buses, tickets, and next_ticket_id
- **Auto-creation**: Generated on first run
- **Encoding**: UTF-8 for proper Bengali text support

### Input Validation

- **Bus Names**: Case-insensitive matching
- **Seat Counts**: Must be positive integers (1-100)
- **Passenger Info**: Non-empty strings required
- **Price Validation**: Positive values only

### Error Handling

- **User-friendly messages**: Clear error dialogs
- **Input validation**: Real-time feedback
- **Graceful failures**: System remains stable
- **Recovery options**: Clear next steps

## 🛠️ Development

### Code Quality

- **Type Hints**: Full type annotations for all functions
- **Clean Architecture**: Separation of concerns
- **Error Handling**: Comprehensive error management
- **Modern Python**: Uses latest language features

### GUI Features

- **Material Design**: Modern dark theme
- **Responsive**: Adapts to different screen sizes
- **Accessible**: Clear labels and intuitive navigation
- **Professional**: Production-ready interface

### Extensibility

The modular design allows easy extension:

- **New GUI tabs**: Add admin panels, reports, etc.
- **Additional features**: Payment processing, notifications
- **Custom themes**: Easy styling modifications
- **Database integration**: Replace JSON with SQL

## 🔄 Data Management

### Real-time Updates

- **Auto-reload**: Every 5 seconds
- **Background sync**: No user intervention
- **Immediate feedback**: Changes appear instantly
- **Data integrity**: Consistent state management

### Resetting Data

To reset to initial state:

1. Delete `data_store.json`
2. Restart the application
3. System will recreate with all 23 preloaded buses

### Data Backup

The `data_store.json` file contains all system data:

- Bus schedules and availability
- All ticket bookings
- Next ticket ID counter

## 🚨 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'PyQt6'"**:

   ```bash
   pip install PyQt6
   ```

2. **"Bus not found"**: Check bus name spelling (case-insensitive)

3. **"Insufficient seats"**: Try fewer seats or different bus

4. **File errors**: Ensure write permissions in directory

5. **Import errors**: Verify all Python files are present

### System Requirements

- **OS**: Windows, macOS, Linux
- **Python**: 3.7+ (tested on 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13)
- **Memory**: ~50MB RAM
- **Disk**: ~10KB for data storage
- **Display**: 800x600 minimum resolution

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please ensure:

- Code follows existing style guidelines
- Type hints are maintained
- Error handling is comprehensive
- GUI remains responsive and accessible
- Documentation is updated

## 📞 Support

For issues or questions:

1. Check the troubleshooting section
2. Verify Python and PyQt6 installation
3. Ensure all files are present
4. Check file permissions

---

**Built with ❤️ for Bangladesh's bus transportation system**

_Modern GUI • Real-time Updates • Professional Interface_
