from PyQt5.QtWidgets import (
    QSizePolicy, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QFrame, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QButtonGroup, QHeaderView, QDialog
)
from PyQt5.QtGui import QColor, QBrush, QPalette, QLinearGradient, QPixmap, QPainter, QFont
from PyQt5.QtCore import Qt
import requests
from windows.rateWindow import RateMovie
from windows.snowflakes import SnowfallBackground

class MovieInfoWindow(QWidget):
    def __init__(self, movie_name, movie_info, username):
        super().__init__()
        self.snowfall_background = SnowfallBackground(self)
        self.snowfall_background.create_snowflakes()
        self.setWindowTitle("Информация о фильме")
        self.resize(800, 800)
        self.movie_name = movie_name
        self.username = username
        clients_info = self.fetch_movie_info(movie_name)

        name_label = QLabel(movie_name)
        name_label.setFont(QFont("Arial", 32))
        session_count_label = QLabel(f"Сеансы: {len(movie_info.get('showTime', []))}")
        seats_label = QLabel(f"Места: {movie_info.get('seats', 'Не указано')}")

        poster_view = self.setup_poster(movie_info.get('poster', ''))
        star_rating_layout = self.create_star_rating()
        

        self.table = self.create_schedule_table(clients_info)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.close)

        rate_button = QPushButton("Оценить")
        rate_button.clicked.connect(self.rate_movie)

        main_layout = QVBoxLayout()
        info_layout = QHBoxLayout()

        movie_info_layout = QVBoxLayout()
        movie_info_layout.addWidget(name_label)
        movie_info_layout.addWidget(session_count_label)
        session_count_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        movie_info_layout.addWidget(seats_label)
        seats_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        session_count_label.setFont(QFont("Arial", 18))
        seats_label.setFont(QFont("Arial", 18))

        movie_info_layout.addLayout(star_rating_layout)

        info_layout.addWidget(poster_view)
        poster_view.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        info_layout.addLayout(movie_info_layout)

        main_layout.addLayout(info_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(rate_button)
        main_layout.addWidget(back_button)

        self.setLayout(main_layout)
        self.set_gradient_background()
        self.update_star_rating()


        rate_button.setStyleSheet(
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

        back_button.setStyleSheet(
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

    def fetch_movie_info(self, movie_name):
        try:
            response = requests.post(
                'https://tochka2802.pythonanywhere.com/movies/getMovieInfo',
                json={'title': movie_name}
            )
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return {}

    def setup_poster(self, poster_url):
        poster_frame = QFrame()
        poster_layout = QVBoxLayout(poster_frame)

        poster_pixmap = QPixmap()
        print(poster_url)
        if poster_url:
            try:
                poster_pixmap.loadFromData(requests.get("https://tochka2802.pythonanywhere.com/" + poster_url).content)                
            except Exception:
                poster_pixmap = self.create_placeholder_pixmap()
        else:
            poster_pixmap = self.create_placeholder_pixmap()

        poster_view = QGraphicsView()
        poster_scene = QGraphicsScene()
        poster_item = QGraphicsPixmapItem(poster_pixmap.scaled(210, 300, Qt.IgnoreAspectRatio ,Qt.SmoothTransformation))
        poster_view.setRenderHint(QPainter.Antialiasing)
        poster_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        poster_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        poster_scene.addItem(poster_item)
        poster_view.setScene(poster_scene)
        poster_view.setFixedSize(210, 300)

        poster_layout.addWidget(poster_view)

        return poster_frame

    def create_placeholder_pixmap(self):
        pixmap = QPixmap(100, 140)
        pixmap.fill(Qt.gray)
        return pixmap

    def create_star_rating(self):
        self.star_label = QLabel("оценка")
        self.star_label.setFont(QFont("Arial", 30))
        star_rating_layout = QHBoxLayout()
        self.star_buttons = QButtonGroup(self)

        for i in range(5):
            star_button = QPushButton("☆")
            star_button.setStyleSheet("font-size: 30px; color: gray; border: none;")
            star_button.setCheckable(True)
            star_button.setMaximumSize(34, 34)
            self.star_buttons.addButton(star_button, i + 1)
            star_rating_layout.addWidget(star_button)

        star_rating_layout.addWidget(self.star_label)
        star_rating_layout.addStretch()
        return star_rating_layout

    def create_schedule_table(self, clients_info):
        table = QTableWidget()
        table.setRowCount(len(clients_info))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Имя", "Время", "Бронь", "Куплено"])

        for i, (name, data) in enumerate(clients_info.items()):
            print(i, name, data)
            try:
                bookedSeats = [num for nums in data['booked'].values() for num in nums]
            except: 
                bookedSeats = []
            try:
                boughtSeats = [num for nums in data['bought'].values() for num in nums]
            except: 
                boughtSeats = []

            time = []
            try:
                for outer_dict in data.values():
                    time.extend(outer_dict.keys())
            except:
                pass

            time = list(set(time))

            table.setItem(i, 0, QTableWidgetItem(name))
            table.setItem(i, 1, QTableWidgetItem(", ".join(time)))
            table.setItem(i, 2, QTableWidgetItem(", ".join(bookedSeats)))
            table.setItem(i, 3, QTableWidgetItem(", ".join(boughtSeats)))
            
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return table

    def set_gradient_background(self):
        gradient = QLinearGradient(self.width(), self.height(), 0, 0)
        gradient.setColorAt(1.0, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.5, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.0, QColor(85, 85, 85, 50))

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def update_star_rating(self):
        response = requests.post("https://tochka2802.pythonanywhere.com/movies/getRating", json={"movie": self.movie_name})
        print(response)
        rating = round(float(response.json().get("rating")))
        self.star_label.setText(str(rating) + "/5")

        for i, button in enumerate(self.star_buttons.buttons()):
            if i + 1 <= rating:
                button.setText("★")
                button.setStyleSheet("font-size: 30px; color: gold; border: none;")
            else:
                button.setText("☆")
                button.setStyleSheet("font-size: 30px; color: gray; border: none;")

    def rate_movie(self):
        rate_window = RateMovie(self.movie_name, self.username, self)
        if rate_window.exec_() == QDialog.Accepted:
            self.update_star_rating()