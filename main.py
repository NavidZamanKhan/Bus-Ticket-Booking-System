from __future__ import annotations

from typing import List

from booking_system import BookingSystem
from bus import Bus


def print_bus_row(bus: Bus) -> None:
    print(
        f"- {bus.name} | {bus.origin} -> {bus.destination} | {bus.departure_time} | "
        f"{bus.price_per_ticket} BDT | Seats: {bus.available_seats}/{bus.total_seats}"
    )


def show_all_available(system: BookingSystem) -> None:
    buses: List[Bus] = system.list_available_buses()
    if not buses:
        print("No buses available right now.")
        return
    print("Available Buses:")
    for b in buses:
        print_bus_row(b)


def search_flow(system: BookingSystem) -> None:
    origin = input("Enter origin: ").strip()
    destination = input("Enter destination: ").strip()
    results = system.search_buses(origin, destination)
    if not results:
        print("No matching buses found.")
        return
    print("Matching Buses:")
    for b in results:
        print_bus_row(b)


def book_flow(system: BookingSystem) -> None:
    bus_name = input("Enter Bus Name: ").strip()
    passenger_name = input("Enter Passenger Name: ").strip()
    contact = input("Enter Contact Number: ").strip()
    try:
        seat_count_str = input("Enter Seat Count: ").strip()
        seat_count = int(seat_count_str)
    except ValueError:
        print("Invalid seat count. Must be a number.")
        return
    try:
        ticket = system.book_ticket(bus_name, passenger_name, contact, seat_count)
    except ValueError as e:
        print(f"Booking failed: {e}")
        return
    print_ticket_receipt(
        ticket.ticket_id,
        passenger_name,
        contact,
        ticket.bus_name,
        ticket.origin,
        ticket.destination,
        ticket.departure_time,
        ticket.seat_count,
        ticket.price_paid,
    )


def print_ticket_receipt(
    ticket_id: int,
    passenger: str,
    contact: str,
    bus_name: str,
    origin: str,
    destination: str,
    departure: str,
    seat_count: int,
    amount_bdt: int,
) -> None:
    print("========== BUS TICKET ==========")
    print(f"Ticket ID     : {ticket_id}")
    print(f"Passenger     : {passenger}")
    print(f"Contact       : {contact}")
    print(f"Bus           : {bus_name}")
    print(f"Route         : {origin} -> {destination}")
    print(f"Departure     : {departure}")
    print(f"Seats         : {seat_count}")
    print(f"Amount Paid   : {amount_bdt} BDT")
    print("================================")


def main() -> None:
    system = BookingSystem()
    while True:
        print("=== Bus Ticket Booking System ===")
        print("1. View Available Buses")
        print("2. Search Buses")
        print("3. Book Ticket")
        print("4. Exit")
        choice = input("Select an option (1-4): ").strip()
        if choice == "1":
            show_all_available(system)
        elif choice == "2":
            search_flow(system)
        elif choice == "3":
            book_flow(system)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-4.")
        print()


if __name__ == "__main__":
    main()
