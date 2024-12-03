import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QPushButton, QVBoxLayout, 
    QHBoxLayout, QLabel, QWidget, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor


class CinemaWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кинотеатр")
        self.resize(600, 400)

        # Create widgets
        self.movie_list = QListWidget()
        self.session_list = QListWidget()

        movies_label = QLabel("Фильмы")
        sessions_label = QLabel("Сеансы")

        self.buy_button = QPushButton("Купить")
        self.info_button = QPushButton("Информация о фильме")
        self.history_button = QPushButton("История")

        # Layout for movies
        movies_layout = QVBoxLayout()
        movies_layout.addWidget(movies_label)
        movies_layout.addWidget(self.movie_list)

        # Layout for sessions
        sessions_layout = QVBoxLayout()
        sessions_layout.addWidget(sessions_label)
        sessions_layout.addWidget(self.session_list)

        # Horizontal layout for lists
        main_layout = QHBoxLayout()
        main_layout.addLayout(movies_layout)
        main_layout.addLayout(sessions_layout)

        # Layout for buttons
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.buy_button)
        button_layout.addWidget(self.info_button)
        button_layout.addWidget(self.history_button)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(main_layout)
        layout.addLayout(button_layout)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Add movies to the list
        self.movie_list.addItems(["Гладиатор 1", "Фильм 2", "Фильм 3"])

        # Connect signals
        self.movie_list.itemClicked.connect(self.display_sessions)
        self.info_button.clicked.connect(self.open_movie_info)

        # Example data
        self.movies_data = {
            "Гладиатор 1": {
                "sessions": ["12:00", "15:00", "18:00"],
                "seats": 1250
            },
            "Фильм 2": {
                "sessions": ["14:00", "18:00"],
                "seats": 800
            },
            "Фильм 3": {
                "sessions": ["16:00", "20:00"],
                "seats": 600
            }
        }

        # Set gradient background
        self.set_gradient_background()

    def set_gradient_background(self):
        """Set a diagonal gradient background."""
        gradient = QLinearGradient(self.width(), self.height(), 0, 0)  # Диагональный градиент
        gradient.setColorAt(1.0, QColor(136,0,0,35))  # Красный оттенок (нижний правый угол)
        gradient.setColorAt(0.0, QColor(85,85,85,0.33))  # Серый оттенок (верхний левый угол)


        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def display_sessions(self, item):
        """Display sessions based on the selected movie."""
        self.session_list.clear()
        movie_name = item.text()
        sessions = self.movies_data.get(movie_name, {}).get("sessions", [])
        self.session_list.addItems(sessions)

    def open_movie_info(self):
        """Open the movie information window."""
        selected_movie = self.movie_list.currentItem()
        selected_time = self.session_list.currentItem()

        if selected_movie and selected_time:
            movie_name = selected_movie.text()
            time = selected_time.text()
            movie_info = self.movies_data.get(movie_name, {})
            self.info_window = MovieInfoWindow(movie_name, time, movie_info)
            self.info_window.show()


class MovieInfoWindow(QWidget):
    def __init__(self, movie_name, time, movie_info):
        super().__init__()
        self.setWindowTitle("Информация о фильме")
        self.resize(500, 300)

        # Movie details
        name_label = QLabel(f"Название: {movie_name}")
        session_count_label = QLabel(f"Сеансы: {len(movie_info['sessions'])}")
        seats_label = QLabel(f"Места: {movie_info['seats']}")

        # Schedule table
        self.table = QTableWidget()
        self.table.setRowCount(len(movie_info["sessions"]))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Название фильма", "Время"])

        # Populate table
        for i, session_time in enumerate(movie_info["sessions"]):
            self.table.setItem(i, 0, QTableWidgetItem(movie_name))
            self.table.setItem(i, 1, QTableWidgetItem(session_time))

        # Back button
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.close)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(session_count_label)
        layout.addWidget(seats_label)
        layout.addWidget(self.table)
        layout.addWidget(back_button)

        self.setLayout(layout)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CinemaWindow()
    window.show()
    sys.exit(app.exec_())
