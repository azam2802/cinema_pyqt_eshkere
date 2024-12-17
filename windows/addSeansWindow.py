from PyQt5.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QLineEdit, QPushButton, QLabel, QSizePolicy
from PyQt5.QtGui import QLinearGradient, QPalette, QBrush, QColor
import requests
from windows.snowflakes import SnowfallBackground

class AddSeansWindow(QDialog):
    def __init__(self, movie, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить сеанс")
        self.snowfall_background = SnowfallBackground(self)
        self.snowfall_background.create_snowflakes()
        self.setFixedSize(300, 300)
        self.movie = movie
        self.text = movie.text()

        layout = QVBoxLayout()

        self.showtime_label = QLabel()
        self.showtime_label.setText(f"Добавить сеансы к фильму {self.text}")
        self.showtime_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(self.showtime_label)

        self.showtime_input = QLineEdit()
        self.showtime_input.setPlaceholderText("Время сеансов через запятую")
        layout.addWidget(self.showtime_input)

        self.add_button = QPushButton("Добавить сеанс")
        
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_seans)
        self.set_gradient_background()
        

        self.add_button.setStyleSheet(
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

    def set_gradient_background(self):
        gradient = QLinearGradient(self.width(), self.height(), 0, 0)
        gradient.setColorAt(1.0, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.5, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.0, QColor(85, 85, 85, 50))

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def add_seans(self):
        showtime = [i.strip() for i in self.showtime_input.text().split(",")]

        if not showtime:
            QMessageBox(Warning, "Empty fields!", "All fields are required!")
            return

        try:
            data = {
                'title': self.text,
                'showTime': showtime, 
            }

            response = requests.post('https://tochka2802.pythonanywhere.com/movies/addShowTime', json=data)
            
            if response.status_code == 200 or response.status_code == 201:
                self.accept()  
    
        except Exception as e:
            print(f"An error occurred: {e}")