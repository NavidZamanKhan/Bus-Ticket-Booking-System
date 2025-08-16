from __future__ import annotations

import sys
from typing import List, Optional, Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from booking_system import BookingSystem
from bus import Bus
from ticket import Ticket


class ReceiptDialog(QDialog):
    def __init__(self, ticket: Ticket, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Bus Ticket Receipt")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        title = QLabel("========== BUS TICKET ==========")
        title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        layout.addWidget(title)
        layout.addWidget(QLabel(f"Ticket ID     : {ticket.ticket_id}"))
        layout.addWidget(QLabel(f"Passenger     : {ticket.passenger_name}"))
        layout.addWidget(QLabel(f"Contact       : {ticket.contact_number}"))
        layout.addWidget(QLabel(f"Bus           : {ticket.bus_name}"))
        layout.addWidget(
            QLabel(f"Route         : {ticket.origin} -> {ticket.destination}")
        )
        layout.addWidget(QLabel(f"Departure     : {ticket.departure_time}"))
        layout.addWidget(QLabel(f"Seats         : {ticket.seat_count}"))
        layout.addWidget(QLabel(f"Amount Paid   : {ticket.price_paid} BDT"))
        footer = QLabel("================================")
        layout.addWidget(footer)
        button_box = QHBoxLayout()
        button_box.addStretch(1)
        ok_btn = QPushButton("Close")
        ok_btn.clicked.connect(self.accept)
        button_box.addWidget(ok_btn)
        layout.addLayout(button_box)
        self.setLayout(layout)


class AvailableBusesTab(QWidget):
    def __init__(self, system: BookingSystem) -> None:
        super().__init__()
        self.system = system
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [
                "Bus Name",
                "Route",
                "Departure",
                "Price (BDT)",
                "Seats (Avail/Total)",
            ]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(refresh_btn)
        self.setLayout(layout)
        self.refresh()

    def refresh(self) -> None:
        buses: List[Bus] = self.system.list_available_buses()
        self.table.setRowCount(len(buses))
        for row, b in enumerate(buses):
            self.table.setItem(row, 0, QTableWidgetItem(b.name))
            self.table.setItem(
                row, 1, QTableWidgetItem(f"{b.origin} -> {b.destination}")
            )
            self.table.setItem(row, 2, QTableWidgetItem(b.departure_time))
            self.table.setItem(row, 3, QTableWidgetItem(str(b.price_per_ticket)))
            self.table.setItem(
                row, 4, QTableWidgetItem(f"{b.available_seats}/{b.total_seats}")
            )


class SearchTab(QWidget):
    def __init__(self, system: BookingSystem) -> None:
        super().__init__()
        self.system = system
        self.origin_input = QLineEdit()
        self.destination_input = QLineEdit()
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [
                "Bus Name",
                "Route",
                "Departure",
                "Price (BDT)",
                "Seats (Avail/Total)",
            ]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        form = QHBoxLayout()
        form.addWidget(QLabel("Origin:"))
        form.addWidget(self.origin_input)
        form.addWidget(QLabel("Destination:"))
        form.addWidget(self.destination_input)
        form.addWidget(self.search_btn)
        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def search(self) -> None:
        origin = self.origin_input.text().strip()
        destination = self.destination_input.text().strip()
        results: List[Bus] = self.system.search_buses(origin, destination)
        self.table.setRowCount(len(results))
        for row, b in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(b.name))
            self.table.setItem(
                row, 1, QTableWidgetItem(f"{b.origin} -> {b.destination}")
            )
            self.table.setItem(row, 2, QTableWidgetItem(b.departure_time))
            self.table.setItem(row, 3, QTableWidgetItem(str(b.price_per_ticket)))
            self.table.setItem(
                row, 4, QTableWidgetItem(f"{b.available_seats}/{b.total_seats}")
            )


class BookTab(QWidget):
    def __init__(
        self, system: BookingSystem, on_refresh: Optional[Callable[[], None]] = None
    ) -> None:
        super().__init__()
        self.system = system
        self.on_refresh = on_refresh
        self.bus_select = QComboBox()
        self.name_input = QLineEdit()
        self.contact_input = QLineEdit()
        self.seat_spin = QSpinBox()
        self.seat_spin.setRange(1, 100)
        self.book_btn = QPushButton("Book Ticket")
        self.book_btn.clicked.connect(self.book)
        form = QVBoxLayout()
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Bus:"))
        row1.addWidget(self.bus_select)
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Passenger Name:"))
        row2.addWidget(self.name_input)
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Contact Number:"))
        row3.addWidget(self.contact_input)
        row4 = QHBoxLayout()
        row4.addWidget(QLabel("Seats:"))
        row4.addWidget(self.seat_spin)
        form.addLayout(row1)
        form.addLayout(row2)
        form.addLayout(row3)
        form.addLayout(row4)
        form.addWidget(self.book_btn)
        self.setLayout(form)
        self.reload_buses()

    def reload_buses(self) -> None:
        self.bus_select.clear()
        for b in self.system.list_available_buses():
            self.bus_select.addItem(
                f"{b.name} ({b.origin}->{b.destination} {b.departure_time})",
                userData=b.name,
            )

    def book(self) -> None:
        bus_name = self.bus_select.currentData()
        passenger = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        count = int(self.seat_spin.value())
        if not bus_name:
            QMessageBox.warning(self, "Validation", "Please select a bus.")
            return
        try:
            ticket = self.system.book_ticket(bus_name, passenger, contact, count)
        except ValueError as e:
            QMessageBox.warning(self, "Booking Failed", str(e))
            return
        self.name_input.clear()
        self.contact_input.clear()
        self.seat_spin.setValue(1)
        self.reload_buses()
        if self.on_refresh:
            self.on_refresh()
        dlg = ReceiptDialog(ticket, self)
        dlg.exec()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Bus Ticket Booking System")
        self.resize(950, 640)
        self.system = BookingSystem()
        self.tabs = QTabWidget()
        self.available_tab = AvailableBusesTab(self.system)
        self.search_tab = SearchTab(self.system)
        self.book_tab = BookTab(self.system, on_refresh=self.available_tab.refresh)
        self.tabs.addTab(self.available_tab, "Available Buses")
        self.tabs.addTab(self.search_tab, "Search")
        self.tabs.addTab(self.book_tab, "Book Ticket")
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        container.setLayout(layout)
        self.setCentralWidget(container)


def run_app() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
