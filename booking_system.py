from __future__ import annotations

import json
import os
from typing import Dict, List, Optional, Tuple

from bus import Bus
from ticket import Ticket


class DataStore:
    def __init__(self, file_path: str = "data_store.json") -> None:
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self) -> None:
        if not os.path.exists(self.file_path):
            self._write({"buses": [], "tickets": [], "next_ticket_id": 1})

    def _read(self) -> Dict:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: Dict) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_buses(self) -> List[Bus]:
        data = self._read()
        return [Bus.from_dict(b) for b in data.get("buses", [])]

    def save_buses(self, buses: List[Bus]) -> None:
        data = self._read()
        data["buses"] = [b.to_dict() for b in buses]
        self._write(data)

    def load_tickets(self) -> List[Ticket]:
        data = self._read()
        return [Ticket.from_dict(t) for t in data.get("tickets", [])]

    def save_tickets(self, tickets: List[Ticket]) -> None:
        data = self._read()
        data["tickets"] = [t.to_dict() for t in tickets]
        self._write(data)

    def get_next_ticket_id(self) -> int:
        data = self._read()
        ticket_id = int(data.get("next_ticket_id", 1))
        data["next_ticket_id"] = ticket_id + 1
        self._write(data)
        return ticket_id


class BookingSystem:
    def __init__(self, store: Optional[DataStore] = None) -> None:
        self.store = store or DataStore()
        self.buses: List[Bus] = self.store.load_buses()
        self.tickets: List[Ticket] = self.store.load_tickets()
        self._preload_if_empty()

    def _preload_if_empty(self) -> None:
        if self.buses:
            return
        demo: List[Tuple[str, str, str, str, int, int]] = [
            ("Ena Transport", "Sylhet", "Dhaka", "08:00", 40, 800),
            ("Hanif Enterprise", "Sylhet", "Chittagong", "09:00", 40, 900),
            ("Shyamoli Paribahan", "Dhaka", "Chittagong", "10:30", 40, 1000),
            ("Desh Travels", "Dhaka", "Sylhet", "11:00", 40, 850),
            ("London Express", "Sylhet", "Cumilla", "14:00", 40, 700),
            ("Saudia Coach", "Sylhet", "Feni", "15:30", 40, 650),
            ("Green Line Paribahan", "Dhaka", "Chittagong", "07:30", 40, 1200),
            ("Shohagh Paribahan", "Dhaka", "Cox's Bazar", "21:00", 40, 1400),
            ("SilkLine", "Sylhet", "Dhaka", "17:45", 40, 800),
            ("Unique Paribahan", "Sylhet", "Chittagong", "06:30", 40, 900),
            ("Year-71 Express", "Sylhet", "Khulna", "16:00", 40, 1300),
            ("Shyamoli NR Travels", "Sylhet", "Jessore", "20:00", 40, 1350),
            ("Ena Transport", "Sylhet", "Rajshahi", "07:45", 40, 1400),
            ("London Express", "Sylhet", "Bogra", "12:30", 40, 1100),
            ("Hanif Enterprise", "Sylhet", "Feni", "13:45", 40, 700),
            ("Desh Travels", "Dhaka", "Rajshahi", "09:15", 40, 1000),
            ("Tungipara Express", "Dhaka", "Gopalganj", "06:45", 40, 600),
            ("S Alam Paribahan", "Chittagong", "Cox's Bazar", "05:30", 40, 900),
            ("Ena Transport", "Sylhet", "Cox's Bazar", "22:15", 40, 1700),
            ("Saintmartin Paribahan", "Dhaka", "Teknaf", "23:00", 40, 1800),
            ("Green Line Paribahan", "Sylhet", "Dhaka", "15:00", 40, 1200),
            ("Shohagh Paribahan", "Sylhet", "Dhaka", "23:45", 40, 900),
            ("Haque Enterprise", "Sylhet", "Moulvibazar", "10:00", 40, 400),
        ]

        self.buses = [
            Bus(
                name=n,
                origin=o,
                destination=d,
                departure_time=t,
                total_seats=s,
                price_per_ticket=p,
            )
            for (n, o, d, t, s, p) in demo
        ]
        self.store.save_buses(self.buses)

    def list_buses(self) -> List[Bus]:
        return list(self.buses)

    def list_available_buses(self) -> List[Bus]:
        return [b for b in self.buses if b.available_seats > 0]

    def search_buses(self, origin: str, destination: str) -> List[Bus]:
        o = origin.strip().lower()
        d = destination.strip().lower()
        return [
            b
            for b in self.buses
            if b.origin.lower() == o and b.destination.lower() == d
        ]

    def get_bus_by_name(self, name: str) -> Optional[Bus]:
        key = name.strip().lower()
        for b in self.buses:
            if b.name.lower() == key:
                return b
        return None

    def book_ticket(
        self,
        bus_name: str,
        passenger_name: str,
        contact: str,
        seat_count: int,
    ) -> Ticket:
        if not passenger_name.strip() or not contact.strip():
            raise ValueError("Passenger name and contact must be non-empty")
        if seat_count <= 0:
            raise ValueError("Seat count must be positive")

        bus = self.get_bus_by_name(bus_name)
        if not bus:
            raise ValueError("Bus not found")
        if not bus.book_seat(seat_count):
            raise ValueError("Insufficient available seats")

        total_price = seat_count * bus.price_per_ticket
        ticket = Ticket(
            ticket_id=self.store.get_next_ticket_id(),
            bus_id=bus.name,
            passenger_name=passenger_name,
            contact_number=contact,
            bus_name=bus.name,
            origin=bus.origin,
            destination=bus.destination,
            departure_time=bus.departure_time,
            seat_count=seat_count,
            price_paid=total_price,
        )

        self.tickets.append(ticket)
        self.store.save_buses(self.buses)
        self.store.save_tickets(self.tickets)
        return ticket

    def cancel_ticket(self, ticket_id: int) -> bool:
        for idx, t in enumerate(self.tickets):
            if t.ticket_id == int(ticket_id):
                bus = self.get_bus_by_name(t.bus_name)
                if bus:
                    bus.refund_seat(t.seat_count)
                del self.tickets[idx]
                self.store.save_buses(self.buses)
                self.store.save_tickets(self.tickets)
                return True
        return False
