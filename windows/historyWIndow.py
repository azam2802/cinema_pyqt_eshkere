from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt
import requests

class HistoryWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("User Booking History")
        self.setGeometry(200, 200, 600, 400)

        # Set up the table widget
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)  # Movie, Showtime, Price, Count, Status
        self.table.setHorizontalHeaderLabels(["Movie", "Showtime", "Seat", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable editing

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Load data from API
        self.load_data()

    def load_data(self):
        """Fetch user history from the API and populate the table."""
        url = "https://tochka2802.pythonanywhere.com/users/getHistory"  # Corrected endpoint
        payload = {"username": self.username}

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                history = response.json().get("history", {})
                print("history\n", history)
                if history:
                    self.populate_table(history)
                else:
                    QMessageBox.information(self, "No History", "No booking history found.")
            else:
                message = response.json().get("message", "Error fetching history")
                QMessageBox.warning(self, "Error", message)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to server: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def populate_table(self, history):
        """Populate the table widget with history data."""
        row = 0
        self.table.setRowCount(0)  # Reset the table before populating
        for movie, movie_history in history.items():
            for action, details in movie_history.items():
                for showtime, seats_data in details.items():
                        self.table.insertRow(row)
                        self.table.setItem(row, 0, QTableWidgetItem(movie))
                        self.table.setItem(row, 1, QTableWidgetItem(showtime))
                        self.table.setItem(row, 2, QTableWidgetItem(', '.join(seats_data)))  # Show the seat count
                        self.table.setItem(row, 3, QTableWidgetItem(action.capitalize()))  # Display "Booked" or "Bought"
                        row += 1
