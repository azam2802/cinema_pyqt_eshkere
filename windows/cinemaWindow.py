from PyQt5.QtWidgets import (
    QMainWindow, QListWidget, QPushButton, QDialog, QVBoxLayout, 
    QHBoxLayout, QLabel, QWidget, QMessageBox
)
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor, QPixmap, QPainter, QRegion, QPen
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import requests
import os
from windows.addSeansWindow import AddSeansWindow
from windows.seatsWindow import SeatsWindow
from windows.moveInfoWindow import MovieInfoWindow
from windows.addMovieWIndow import AddMovieWindow
from windows.profileWindow import UserProfile
from windows.historyWIndow import HistoryWindow
from windows.snowflakes import SnowfallBackground

class CinemaWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Кинотеатр")
        self.resize(800, 600)
        self.username = username
        self.original_avatar = None  

        self.music_player = QMediaPlayer()
        music_path = os.path.join(os.path.dirname(__file__), 'music.mp3')
        self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile(music_path)))
        self.music_player.play()
        self.music_player.mediaStatusChanged.connect(self.handle_media_status)

        self.movie_list = QListWidget()
        self.session_list = QListWidget()

        self.snowfall_background = SnowfallBackground(self) 

        movies_label = QLabel("Фильмы")
        sessions_label = QLabel("Сеансы")

        self.buy_button = self.create_styled_button("Купить")
        self.history_button = self.create_styled_button("История")
        self.add_movie_button = self.create_styled_button("Добавить фильм")
        self.info_button = self.create_styled_button("Информация о фильме")
        self.add_session_button = self.create_styled_button("Добавить сеанс")
        self.delete_movie_button = self.create_styled_button("Удалить фильм")

        self.delete_movie_button.hide()
        self.add_session_button.hide()
        if username != 'admin':
            self.add_movie_button.hide()
        self.buy_button.hide()
        self.info_button.hide()

        self.history_button.setProperty("margin", "true")

        self.buy_button.clicked.connect(self.open_seats_window)
        self.info_button.clicked.connect(self.open_movie_info)
        self.history_button.clicked.connect(self.open_history_window)
        self.add_movie_button.clicked.connect(self.open_add_movie_window)
        self.add_session_button.clicked.connect(self.open_add_session_window)
        self.delete_movie_button.clicked.connect(self.delete_movie)

        self.profile_label = QLabel()
        self.profile_label.setFixedSize(50, 50)
        self.update_avatar()
        self.profile_label.mousePressEvent = self.open_profile_window

        top_bar_layout = QHBoxLayout()
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.profile_label)

        self.username_display = QLabel(self.username)
        self.username_display.setStyleSheet("""
            color: white; 
            font-size: 18px; 
            text-decoration: underline;
        """)
        self.username_display.mousePressEvent = self.open_profile_window

        top_bar_layout.addWidget(self.username_display)

        movies_layout = QVBoxLayout()
        movies_layout.addWidget(movies_label)
        movies_layout.addWidget(self.movie_list)

        sessions_layout = QVBoxLayout()
        sessions_layout.addWidget(sessions_label)
        sessions_layout.addWidget(self.session_list)

        lists_layout = QHBoxLayout()
        lists_layout.addLayout(movies_layout)
        lists_layout.addLayout(sessions_layout)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(5)
        button_layout.addStretch()
        button_layout.addWidget(self.buy_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.history_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.info_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.add_movie_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.add_session_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.delete_movie_button, alignment=Qt.AlignCenter)
        button_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_bar_layout)
        main_layout.addLayout(lists_layout)
        main_layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.set_gradient_background()
        self.movie_list.itemClicked.connect(self.onRowSelection)

        self.movies_data = {}
        self.fetch_movies()

        self.movie_list.setStyleSheet(
            "border: 1px solid transparent; border-radius: 10px; background-color: rgba(0, 0, 0, 0.5); padding: 5px;"
        )
        self.session_list.setStyleSheet(
            "border: 1px solid transparent; border-radius: 10px; background-color: rgba(0, 0, 0, 0.5); padding: 5px;"
        )
        self.snowfall_background.create_snowflakes() 

        self.raise_()

    def closeEvent(self, event):
        self.music_player.stop()
        super().closeEvent(event)

    def onRowSelection(self, item):
        self.display_sessions(item)
        self.info_button.show()
        self.buy_button.show()
        if self.username == "admin":
            self.delete_movie_button.show()
            self.add_session_button.show()

    def create_styled_button(self, text):
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
        gradient = QLinearGradient(self.width(), self.height(), 0, 0)
        gradient.setColorAt(1.0, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.5, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.0, QColor(85, 85, 85, 50))

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def fetch_movies(self, ):
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
        self.session_list.clear()
        movie_name = item.text()
        sessions = self.movies_data.get(movie_name, {}).get("showTime", [])
        print(sessions)
        for session in sessions:
            self.session_list.addItem(session)

    def open_movie_info(self):
        selected_movie = self.movie_list.currentItem()

        if selected_movie:
            movie_name = selected_movie.text()
            movie_info = self.movies_data.get(movie_name, {})
            self.info_window = MovieInfoWindow(movie_name, movie_info, self.username)
            self.info_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите фильм.")

    def open_seats_window(self):
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
        add_movie_window = AddMovieWindow(self)
        if add_movie_window.exec_() == QDialog.Accepted:
            self.fetch_movies()

    def open_add_session_window(self):
        item = self.movie_list.currentItem()
        add_movie_window = AddSeansWindow(item, self)
        if add_movie_window.exec_() == QDialog.Accepted:
            self.fetch_movies()
            self.session_list.clear()

    def delete_movie(self):
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
        self.history_window = HistoryWindow(self.username)
        self.history_window.show()

    def open_profile_window(self, _):
        if not hasattr(self, 'user_profile'):
            user_profile = UserProfile(self.username, self.original_avatar, self)
            if user_profile.exec_() == QDialog.Accepted:
                self.update_avatar()

    def update_avatar(self):
        try:
            response = requests.post("https://tochka2802.pythonanywhere.com/users/getAvatar", json={"username": self.username})
            print(response.status_code, response.json())
            if response.ok:
                avatar_path = response.json().get("avatar")
                base_url = "https://tochka2802.pythonanywhere.com/"
                full_avatar_url = base_url + avatar_path
                
                img_response = requests.get(full_avatar_url)
                if img_response.ok:
                    pixmap = QPixmap()
                    pixmap.loadFromData(img_response.content)
                    self.original_avatar = pixmap
                    
                    size = 400  
                    scaled_pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                    
                    mask = QPixmap(size, size)
                    mask.fill(Qt.transparent)
                    painter = QPainter(mask)
                    painter.setRenderHint(QPainter.Antialiasing, True)
                    painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
                    painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
                    
                    painter.setCompositionMode(QPainter.CompositionMode_Source)
                    painter.setBrush(Qt.black)
                    painter.setPen(QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    painter.drawEllipse(0, 0, size, size)
                    painter.end()
                    
                    result = QPixmap(size, size)
                    result.fill(Qt.transparent)
                    painter = QPainter(result)
                    painter.setRenderHint(QPainter.Antialiasing, True)
                    painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
                    painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
                    
                    painter.setCompositionMode(QPainter.CompositionMode_Source)
                    painter.setClipRegion(QRegion(mask.mask()))
                    painter.drawPixmap(0, 0, scaled_pixmap)
                    painter.end()
                    
                    final_pixmap = result.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    
                    self.profile_label.setPixmap(final_pixmap)
                    self.profile_label.setStyleSheet("""
                        QLabel {
                            background: transparent;
                            border-radius: 20px;
                        }
                    """)
        except Exception as e:
            print(f"Error updating avatar: {e}")

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.music_player.play()