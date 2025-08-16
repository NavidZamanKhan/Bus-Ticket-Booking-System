from __future__ import annotations

import sys
from typing import List, Optional, Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QGraphicsDropShadowEffect,
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
        self.setMinimumWidth(420)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        title = QLabel("Ticket Receipt")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.DemiBold))
        layout.addWidget(title)
        info = [
            ("Ticket ID", str(ticket.ticket_id)),
            ("Passenger", ticket.passenger_name),
            ("Contact", ticket.contact_number),
            ("Bus", ticket.bus_name),
            ("Route", f"{ticket.origin} -> {ticket.destination}"),
            ("Departure", ticket.departure_time),
            ("Seats", str(ticket.seat_count)),
            ("Amount Paid", f"{ticket.price_paid} BDT"),
        ]
        for key, val in info:
            row = QHBoxLayout()
            k = QLabel(f"{key}")
            k.setMinimumWidth(110)
            k.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
            v = QLabel(val)
            row.addWidget(k)
            row.addWidget(v)
            row.addStretch(1)
            layout.addLayout(row)
        button_box = QHBoxLayout()
        button_box.addStretch(1)
        ok_btn = QPushButton("Close")
        ok_btn.clicked.connect(self.accept)
        button_box.addWidget(ok_btn)
        layout.addLayout(button_box)
        container = QWidget()
        container.setLayout(layout)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(18)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 160))
        container.setGraphicsEffect(shadow)
        outer = QVBoxLayout()
        outer.addWidget(container)
        self.setLayout(outer)


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
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
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
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
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
    _apply_material_dark_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


def _apply_material_dark_theme(app: QApplication) -> None:
    app.setStyle("Fusion")
    palette = QPalette()
    bg = QColor(30, 32, 34)
    base = QColor(38, 41, 45)
    alt = QColor(44, 47, 51)
    text = QColor(220, 220, 220)
    accent = QColor(98, 0, 238)
    palette.setColor(QPalette.ColorRole.Window, bg)
    palette.setColor(QPalette.ColorRole.WindowText, text)
    palette.setColor(QPalette.ColorRole.Base, base)
    palette.setColor(QPalette.ColorRole.AlternateBase, alt)
    palette.setColor(QPalette.ColorRole.ToolTipBase, base)
    palette.setColor(QPalette.ColorRole.ToolTipText, text)
    palette.setColor(QPalette.ColorRole.Text, text)
    palette.setColor(QPalette.ColorRole.Button, alt)
    palette.setColor(QPalette.ColorRole.ButtonText, text)
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 85, 85))
    palette.setColor(QPalette.ColorRole.Highlight, accent)
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    stylesheet = """
    QWidget { color: #E0E0E0; font-family: 'Segoe UI', 'Inter', sans-serif; }
    QMainWindow, QWidget { background-color: #1E2022; }
    QTabWidget::pane { border: 1px solid #2C2F33; border-radius: 8px; padding: 4px; }
    QTabBar::tab { background: #2C2F33; border: 1px solid #2C2F33; border-bottom: none; padding: 8px 14px; margin-right: 6px; border-top-left-radius: 8px; border-top-right-radius: 8px; }
    QTabBar::tab:selected { background: #3A3E44; color: #FFFFFF; }
    QTabBar::tab:hover { background: #34383D; }
    QPushButton { background-color: #6200EE; color: white; border: none; border-radius: 8px; padding: 8px 14px; }
    QPushButton:hover { background-color: #7C33F0; }
    QPushButton:pressed { background-color: #4A00C8; }
    QPushButton:disabled { background-color: #3A3E44; color: #9AA0A6; }
    QLineEdit, QComboBox, QSpinBox { background: #26292D; border: 1px solid #2C2F33; border-radius: 8px; padding: 6px 8px; }
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border: 1px solid #6200EE; }
    QTableWidget { background: #26292D; alternate-background-color: #2C2F33; gridline-color: #2C2F33; selection-background-color: #6200EE; selection-color: #FFFFFF; }
    QHeaderView::section { background-color: #2C2F33; color: #E0E0E0; padding: 6px; border: none; border-right: 1px solid #1E2022; }
    QTableWidget::item { padding: 6px; }
    """
    app.setStyleSheet(stylesheet)
