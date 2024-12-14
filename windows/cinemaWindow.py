from PyQt5.QtWidgets import (
    QMainWindow, QListWidget, QPushButton, QDialog, QVBoxLayout, 
    QHBoxLayout, QLabel, QWidget, QMessageBox
)
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import Qt
import requests
from windows.seatsWindow import SeatsWindow
from windows.moveInfoWindow import MovieInfoWindow
from windows.addMovieWIndow import AddMovieWindow
from windows.profileWindow import UserProfile
from windows.historyWIndow import HistoryWindow

class CinemaWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Кинотеатр")
        self.resize(800, 600)
        self.username = username
        # Create widgets
        self.movie_list = QListWidget()
        self.session_list = QListWidget()

        movies_label = QLabel("Фильмы")
        sessions_label = QLabel("Сеансы")

        self.buy_button = self.create_styled_button("Купить")
        self.info_button = self.create_styled_button("Информация о фильме")
        self.history_button = self.create_styled_button("История")
        self.add_movie_button = self.create_styled_button("Добавить фильм")
        self.delete_movie_button = self.create_styled_button("Удалить фильм")

        self.buy_button.clicked.connect(self.open_seats_window)
        self.info_button.clicked.connect(self.open_movie_info)
        self.history_button.clicked.connect(self.open_history_window)
        self.add_movie_button.clicked.connect(self.open_add_movie_window)
        self.delete_movie_button.clicked.connect(self.delete_movie)

        # Profile Button (Circular)
        self.profile_button = QPushButton()
        self.profile_button.setFixedSize(50, 50)
        self.profile_button.setStyleSheet(
            "background-color: gray; border-radius: 25px; border: none;"
        )
        self.profile_button.clicked.connect(self.open_profile_window)

        # Top bar layout for profile button
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.profile_button)

        # Layout for movies and sessions
        movies_layout = QVBoxLayout()
        movies_layout.addWidget(movies_label)
        movies_layout.addWidget(self.movie_list)

        # Layout for sessions
        sessions_layout = QVBoxLayout()
        sessions_layout.addWidget(sessions_label)
        sessions_layout.addWidget(self.session_list)

        lists_layout = QHBoxLayout()
        lists_layout.addLayout(movies_layout)
        lists_layout.addLayout(sessions_layout)

        # Layout for buttons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(5)
        button_layout.addStretch()
        button_layout.addWidget(self.buy_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.info_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.history_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.add_movie_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.delete_movie_button, alignment=Qt.AlignCenter)
        button_layout.addStretch()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_bar_layout)
        main_layout.addLayout(lists_layout)
        main_layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Set gradient background
        self.set_gradient_background()
        self.movie_list.itemClicked.connect(self.display_sessions)

        # Fetch movie data
        self.movies_data = {}
        self.fetch_movies()

        # Apply styles to lists
        self.movie_list.setStyleSheet(
            "border: 1px solid transparent; border-radius: 10px; background-color: rgba(0, 0, 0, 0.5); padding: 5px;"
        )
        self.session_list.setStyleSheet(
            "border: 1px solid transparent; border-radius: 10px; background-color: rgba(0, 0, 0, 0.5); padding: 5px;"
        )

    def create_styled_button(self, text):
        """Helper method to create styled buttons."""
        button = QPushButton(text)
        button.setFixedSize(295, 35)
        button.setStyleSheet(
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
        return button

    def set_gradient_background(self):
        """Set a diagonal gradient background."""
        gradient = QLinearGradient(self.width(), self.height(), 0, 0)
        gradient.setColorAt(1.0, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.5, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.0, QColor(85, 85, 85, 50))

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def fetch_movies(self):
        """Fetch movies from backend and update the movie list."""
        response = requests.get('https://tochka2802.pythonanywhere.com/movies/getMovies')
        print(response.json())
        if response.status_code == 200:
            movie_data = response.json()
            self.movie_list.clear()
            self.movies_data = {movie['title']: movie for movie in movie_data}
            movie_names = [movie['title'] for movie in movie_data]
            self.movie_list.addItems(movie_names)
        else:
            print("Error fetching movie data")

    def display_sessions(self, item):
        """Display sessions for the selected movie."""
        self.session_list.clear()
        movie_name = item.text()
        sessions = self.movies_data.get(movie_name, {}).get("showTime", [])
        print(sessions)

        for session in sessions:
            self.session_list.addItem(session)

    def open_movie_info(self):
        """Open the movie information window."""
        selected_movie = self.movie_list.currentItem()
        selected_session = self.session_list.currentItem()

        if selected_movie and selected_session:
            movie_name = selected_movie.text()
            session_time = selected_session.text()
            movie_info = self.movies_data.get(movie_name, {})
            self.info_window = MovieInfoWindow(movie_name, session_time, movie_info)
            self.info_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите фильм и сеанс.")

    def open_seats_window(self):
        """Open the seats window."""
        selected_movie = self.movie_list.currentItem()
        selected_session = self.session_list.currentItem()

        if selected_movie and selected_session:
            movie_name = selected_movie.text()
            session_time = selected_session.text()
            self.seats_window = SeatsWindow(movie_name, session_time, self.username)
            self.seats_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите фильм и сеанс.")

    def open_add_movie_window(self):
        """Open the Add Movie window."""
        add_movie_window = AddMovieWindow(self)
        if add_movie_window.exec_() == QDialog.Accepted:
            self.fetch_movies()

    def delete_movie(self):
        """Delete the selected movie."""
        selected_movie = self.movie_list.currentItem()
        if not selected_movie:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите фильм для удаления.")
            return

        movie_name = selected_movie.text()
        confirmation = QMessageBox.question(
            self, "Подтвердите удаление",
            f"Вы уверены, что хотите удалить фильм '{movie_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            response = requests.post(
                'https://tochka2802.pythonanywhere.com/movies/deleteMovie',
                json={"title": movie_name}
            )
            if response.status_code == 200:
                self.fetch_movies()
                self.session_list.clear()
                QMessageBox.information(self, "Успех", "Фильм удален.")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить фильм.")

    def open_history_window(self):
        """Open the history window."""
        self.history_window = HistoryWindow(self.username)
        self.history_window.show()
    def open_profile_window(self):
        """Open the profile window."""
        if not hasattr(self, 'user_profile'):
            self.user_profile = UserProfile()
        self.user_profile.show()
    