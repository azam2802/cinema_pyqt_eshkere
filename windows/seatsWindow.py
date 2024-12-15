from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel,
    QVBoxLayout, QWidget, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QLinearGradient, QColor, QPalette, QBrush
import requests
from windows.snowflakes import SnowfallBackground

class SeatsWindow(QMainWindow):
    def __init__(self, movie_name, session_time, username):
        super().__init__()
        self.setWindowTitle("Выбор мест")
        self.resize(800, 600)
        self.snowfall_background = SnowfallBackground(self)
        self.snowfall_background.create_snowflakes()
        self.movie_name = movie_name
        self.session_time = session_time
        self.username = username
        self.selected_seat = None                                                                                                        

        main_layout = QVBoxLayout()
  
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)


        buy_ticket_label = QLabel("Купить билет")
        buy_ticket_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(buy_ticket_label)
        buy_ticket_label.setFont(QFont("Montserrat", 30))


        header_layout.addStretch()

        # Create a vertical layout for color labels
        color_labels_layout = QVBoxLayout()
        color_labels_layout.setAlignment(Qt.AlignCenter)  # Align the labels vertically in the center
        
        # Create the color labels and add them to the vertical layout
        self.create_color_label(color_labels_layout, "Куплено", "green")
        self.create_color_label(color_labels_layout, "Забронировано", "orange")
        self.create_color_label(color_labels_layout, "Свободно", "white")

        # Add the color labels vertical layout to the header layout
        header_layout.addLayout(color_labels_layout)

        # Set the contents margins to add distance between labels
        header_layout.setContentsMargins(50, 0, 0, 0)  # Adjust right margin for spacing

        main_layout.addLayout(header_layout)

        # Add Screen Label
        screen_label = QLabel("Экран")
        screen_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(screen_label, alignment=Qt.AlignCenter)

        # Create the seat rows layout
        self.seat_rows_layout = QVBoxLayout()
        self.seat_rows_layout.setAlignment(Qt.AlignCenter)  # Center all rows
        main_layout.addLayout(self.seat_rows_layout)

        # Buttons for booking and purchasing (arranged vertically and centered)
        button_layout = QVBoxLayout()
        self.reserve_button = QPushButton("Забронировать")
        self.buy_button = QPushButton("Купить")
        self.back_button = QPushButton("Назад")
        button_layout.addWidget(self.reserve_button)
        button_layout.addWidget(self.buy_button)
        button_layout.addWidget(self.back_button)
        main_layout.addLayout(button_layout)
    

        for i in [self.reserve_button, self.buy_button, self.back_button]:
            i.setStyleSheet(
                  """
            QPushButton {
                background-color: rgba(0, 0, 0, 75);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 100);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 100);
            }
            """
            )

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create seats
        self.create_seats()
        self.color_seats()

        # Connect signals
        self.reserve_button.clicked.connect(self.reserve_seat)
        self.buy_button.clicked.connect(self.show_buy_window)
        self.back_button.clicked.connect(self.close)
        self.set_gradient_background()

    def color_seats(self):
        response = requests.post("https://tochka2802.pythonanywhere.com/movies/getSeats", json={"movie": self.movie_name, "showtime": self.session_time})
        print(self.session_time)
        print(self.movie_name)
        print("color", response.json())
        for seat, button in self.seats.items():
            if str(seat) in response.json()["data"]["booked"]:
                button.setDisabled(True)
                button.setStyleSheet("background-color: orange; border: 1px solid black; border-radius: 5px; color: black")

        for seat, button in self.seats.items():
            if str(seat) in response.json()["data"]["bought"]:
                button.setDisabled(True)
                button.setStyleSheet("background-color: green; border: 1px solid black; border-radius: 5px; color: black")


    def set_gradient_background(self):
        """Set a diagonal gradient background."""
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor(85, 85, 85, 50))
        gradient.setColorAt(0.5, QColor(136, 0, 0, 100))
        gradient.setColorAt(1.0, QColor(136, 0, 0, 100))

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)


    def create_seats(self):
        """Create a grid of seats."""
        self.seats = {}
        rows = [9, 11, 13, 15]  
        seat_number = 1  

        for num_seats in rows:
            row_layout = QHBoxLayout()  
            row_layout.setAlignment(Qt.AlignCenter) 

            for _ in range(num_seats):
                seat_button = QPushButton(f"{seat_number}")
                seat_button.setFixedSize(40, 40)
                seat_button.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 5px; color: black")
                seat_button.clicked.connect(lambda _, num=seat_number: self.select_seat(num))
                row_layout.addWidget(seat_button)
                self.seats[seat_number] = seat_button
                seat_number += 1
            
            
            self.seat_rows_layout.addLayout(row_layout)

    def create_color_label(self, layout, text, color):
        """Create a color label for seat status."""
        label = QLabel()
        label.setFixedSize(20, 20)
        label.setStyleSheet(f"background-color: {color}; border: 1px solid black; color: black")
        layout.addWidget(label)
        layout.addWidget(QLabel(text))

    def select_seat(self, seat_number):
        """Select a seat."""
        self.selected_seat = seat_number
        for seat, button in self.seats.items():
            if seat == seat_number:
                button.setStyleSheet("background-color: lightblue; border: 2px solid blue; border-radius: 5px; color: black")
            elif button.styleSheet() == "background-color: lightblue; border: 2px solid blue; border-radius: 5px; color: black":
                button.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 5px; color: black")

    def reserve_seat(self):
        """Reserve the selected seat."""
        if self.selected_seat:
            button = self.seats[self.selected_seat]
            requests.post("https://tochka2802.pythonanywhere.com/users/addHistory", json={"username": self.username, "movie": self.movie_name, "showtime": self.session_time, "seat": str(self.selected_seat), "type": "booked"})
            button.setStyleSheet("background-color: orange; border: 1px solid black; border-radius: 5px; color: black")
            self.selected_seat = None
            self.color_seats()


    def show_buy_window(self):
        """Show confirmation dialog for seat purchase."""
        if not self.selected_seat:
            QMessageBox.warning(self, "Ошибка", "Выберите место для покупки.")
            return

        dialog = QMessageBox(self)
        dialog.setWindowTitle("Покупка места")
        dialog.setText(f"Купить место {self.selected_seat}?")
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.Yes)

        result = dialog.exec_()
        if result == QMessageBox.Yes:
            button = self.seats[self.selected_seat]
            requests.post("https://tochka2802.pythonanywhere.com/users/addHistory", json={"username": self.username, "movie": self.movie_name, "showtime": self.session_time, "seat": str(self.selected_seat), "type": "bought"})
            button.setStyleSheet("background-color: green; border: 1px solid black; border-radius: 5px; color: black")
            QMessageBox.information(self, "Успех", f"Место {self.selected_seat} успешно куплено!")
            self.color_seats()
            self.selected_seat = None
