from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Ticket:
    ticket_id: int
    bus_id: str
    passenger_name: str
    contact_number: str
    bus_name: str
    origin: str
    destination: str
    departure_time: str
    seat_count: int
    price_paid: int

    def __init__(
        self,
        ticket_id: int,
        bus_id: str,
        passenger_name: str,
        contact_number: str,
        bus_name: str,
        origin: str,
        destination: str,
        departure_time: str,
        seat_count: int,
        price_paid: int,
    ) -> None:
        if seat_count <= 0:
            raise ValueError("Seat count must be positive")
        if price_paid < 0:
            raise ValueError("Price paid cannot be negative")

        self.ticket_id = int(ticket_id)
        self.bus_id = bus_id
        self.passenger_name = passenger_name.strip()
        self.contact_number = contact_number.strip()
        self.bus_name = bus_name.strip()
        self.origin = origin.strip()
        self.destination = destination.strip()
        self.departure_time = departure_time.strip()
        self.seat_count = int(seat_count)
        self.price_paid = int(price_paid)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticket_id": self.ticket_id,
            "bus_id": self.bus_id,
            "passenger_name": self.passenger_name,
            "contact_number": self.contact_number,
            "bus_name": self.bus_name,
            "origin": self.origin,
            "destination": self.destination,
            "departure_time": self.departure_time,
            "seat_count": self.seat_count,
            "price_paid": self.price_paid,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Ticket":
        return Ticket(
            ticket_id=int(data["ticket_id"]),
            bus_id=data["bus_id"],
            passenger_name=data["passenger_name"],
            contact_number=data["contact_number"],
            bus_name=data["bus_name"],
            origin=data["origin"],
            destination=data["destination"],
            departure_time=data["departure_time"],
            seat_count=int(data["seat_count"]),
            price_paid=int(data["price_paid"]),
        )


