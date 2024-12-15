from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QButtonGroup, QWidget
from PyQt5.QtGui import QLinearGradient, QPalette, QBrush, QColor, QFont
from PyQt5.QtCore import Qt
import requests
from windows.snowflakes import SnowfallBackground

class RateMovie(QDialog):
    def __init__(self, movie, username, parent=None):
        super().__init__(parent)
        self.movie = movie
        self.snowfall_background = SnowfallBackground(self)
        self.snowfall_background.create_snowflakes()
        self.setWindowTitle(f"Оценить {movie}")
        self.setFixedSize(350, 200)
        self.username = username

        layout = QVBoxLayout()

        self.add_button = QPushButton("Оценить")
    
        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_rate)
        self.set_gradient_background()

        star_rating_layout = self.create_star_rating()
        self.container_widget = QWidget()

        self.container_widget.setLayout(star_rating_layout)
        layout.addWidget(self.container_widget, alignment=Qt.AlignCenter)
        layout.addWidget(self.add_button)


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


    def create_star_rating(self):
        """Create a star rating layout."""
        self.star_label = QLabel("0")
        self.star_label.setFont(QFont("Arial", 30))
        star_rating_layout = QHBoxLayout()
        self.star_buttons = QButtonGroup(self)

        for i in range(5):
            star_button = QPushButton("☆")
            star_button.setStyleSheet("font-size: 30px; color: gray; border: none;")
            star_button.clicked.connect(self.rate_movie)
            star_button.setCheckable(True)
            star_button.setMaximumSize(34, 34)
            self.star_buttons.addButton(star_button, i + 1)
            star_rating_layout.addWidget(star_button)

        star_rating_layout.addWidget(self.star_label)
        star_rating_layout.addStretch()

        return star_rating_layout


    def rate_movie(self):
        """Update the star rating based on user interaction."""
        selected_rating = self.star_buttons.checkedId()
        self.star_label.setText(str(selected_rating))
        for i, button in enumerate(self.star_buttons.buttons()):
            if i + 1 <= selected_rating:
                button.setText("★")
                button.setStyleSheet("font-size: 30px; color: gold; border: none;")
            else:
                button.setText("☆")
                button.setStyleSheet("font-size: 30px; color: gray; border: none;")


    def set_gradient_background(self):
        """Set a diagonal gradient background."""
        gradient = QLinearGradient(self.width(), self.height(), 0, 0)
        gradient.setColorAt(1.0, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.5, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.0, QColor(85, 85, 85, 50))

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def add_rate(self):
        selected_rating = self.star_buttons.checkedId()
        print(selected_rating)

        try:
            data = {
                'rate': selected_rating,
                'movie': self.movie, 
                'username': self.username
            }

            response = requests.post('https://tochka2802.pythonanywhere.com/movies/addRating', json=data)
            
            if response.status_code == 200 or response.status_code == 201:
                self.accept()  
    
        except Exception as e:
            print(f"An error occurred: {e}")