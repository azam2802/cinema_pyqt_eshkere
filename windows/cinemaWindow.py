from PyQt5.QtWidgets import QMainWindow, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor
import requests

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
        response = requests.get('http://127.0.0.1:5000/movies/names')
        if response.status_code == 200 or response.status_code == 201:
            movie_names = response.json()
            self.movie_list.addItems(movie_names)
        else:
            print("Error fetching movie names:", response.status_code)

        # Connect signals
        self.movie_list.itemClicked.connect(self.display_sessions)
        self.info_button.clicked.connect(self.open_movie_info)

        # Example data
        self.movies_data = {}

        response = requests.get('http://127.0.0.1:5000/movies/getMovies')
        if response.status_code == 200:
            movies_data = response.json()
            self.movies_data = {movie["title"]: movie for movie in movies_data}
            print(self.movies_data)
        else:
            print("Error fetching movies data:", response.status_code)

        # Apply styles with border and background color
        self.movie_list.setStyleSheet("border: 1px solid transparent; border-radius: 10px; background-color: rgba(0, 0, 0, 0.5); padding: 5px;")
        self.session_list.setStyleSheet("border: 1px solid transparent; border-radius: 10px; background-color: rgba(0, 0, 0, 0.5); padding: 5px;")

        # Set gradient background
        self.set_gradient_background()

    def set_gradient_background(self):
        """Set a diagonal gradient background."""
        gradient = QLinearGradient(self.width(), self.height(), 0, 0)  
        gradient.setColorAt(1.0, QColor(136,0,0,100))
        gradient.setColorAt(0.5, QColor(136,0,0,100)) 
        gradient.setColorAt(0.0, QColor(85,85,85,50)) 


        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def display_sessions(self, item):
        """Display sessions based on the selected movie."""
        self.session_list.clear()
        movie_name = item.text()
        print(self.movies_data)
        sessions = self.movies_data.get(movie_name, {}).get("showTime", [])
        self.session_list.addItems(sessions)

    def open_movie_info(self):
        """Open the movie information window."""
        from windows.moveInfoWindow import MovieInfoWindow
        selected_movie = self.movie_list.currentItem()
        selected_time = self.session_list.currentItem()

        if selected_movie and selected_time:
            movie_name = selected_movie.text()
            time = selected_time.text()
            movie_info = self.movies_data.get(movie_name, {})
            self.info_window = MovieInfoWindow(movie_name, time, movie_info)
            self.info_window.show()