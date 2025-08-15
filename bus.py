from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Bus:
    name: str
    origin: str
    destination: str
    departure_time: str
    total_seats: int
    price_per_ticket: int
    available_seats: int

    def __init__(
        self,
        name: str,
        origin: str,
        destination: str,
        departure_time: str,
        total_seats: int,
        price_per_ticket: int,
        available_seats: Optional[int] = None,
    ) -> None:
        if not name.strip():
            raise ValueError("Bus name must be a non-empty string")
        if not origin.strip() or not destination.strip():
            raise ValueError("Origin and destination must be non-empty strings")
        if total_seats <= 0:
            raise ValueError("Total seats must be a positive integer")
        if price_per_ticket <= 0:
            raise ValueError("Price per ticket must be a positive integer")

        self.name = name.strip()
        self.origin = origin.strip()
        self.destination = destination.strip()
        self.departure_time = departure_time.strip()
        self.total_seats = int(total_seats)
        self.price_per_ticket = int(price_per_ticket)
        self.available_seats = (
            int(available_seats) if available_seats is not None else int(total_seats)
        )
        if self.available_seats < 0 or self.available_seats > self.total_seats:
            raise ValueError("Available seats must be between 0 and total seats")

    def get_available_seats(self) -> int:
        return self.available_seats

    def book_seat(self, count: int) -> bool:
        if count <= 0:
            return False
        if self.available_seats >= count:
            self.available_seats -= count
            return True
        return False

    def refund_seat(self, count: int) -> bool:
        if count <= 0:
            return False
        if self.available_seats + count <= self.total_seats:
            self.available_seats += count
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "origin": self.origin,
            "destination": self.destination,
            "departure_time": self.departure_time,
            "total_seats": self.total_seats,
            "price_per_ticket": self.price_per_ticket,
            "available_seats": self.available_seats,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Bus":
        return Bus(
            name=data["name"],
            origin=data["origin"],
            destination=data["destination"],
            departure_time=data["departure_time"],
            total_seats=int(data["total_seats"]),
            price_per_ticket=int(data["price_per_ticket"]),
            available_seats=int(
                data.get("available_seats", data.get("total_seats", 0))
            ),
        )
