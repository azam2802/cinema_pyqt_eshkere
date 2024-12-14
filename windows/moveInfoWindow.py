from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QFrame, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QButtonGroup
)
from PyQt5.QtGui import QColor, QBrush, QPalette, QLinearGradient, QPixmap, QPainter
from PyQt5.QtCore import Qt
import requests

class MovieInfoWindow(QWidget):
    def __init__(self, movie_name, time, movie_info):
        super().__init__()
        self.setWindowTitle("Информация о фильме")
        self.resize(600, 400)

        clients_info = self.fetch_movie_info(movie_name)

        # Movie details
        name_label = QLabel(f"Название: {movie_name}")
        session_count_label = QLabel(f"Сеансы: {len(movie_info.get('showTime', []))}")
        seats_label = QLabel(f"Места: {movie_info.get('seats', 'Не указано')}")

        # Poster setup
        poster_view = self.setup_poster(movie_info.get('poster', ''))

        # Star rating
        star_rating_layout = self.create_star_rating()

        # Schedule table
        self.table = self.create_schedule_table(clients_info)

        # Back button
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.close)

        # Layout setup
        main_layout = QVBoxLayout()
        info_layout = QHBoxLayout()

        movie_info_layout = QVBoxLayout()
        movie_info_layout.addWidget(name_label)
        movie_info_layout.addWidget(session_count_label)
        movie_info_layout.addWidget(seats_label)
        movie_info_layout.addLayout(star_rating_layout)

        info_layout.addWidget(poster_view)
        info_layout.addLayout(movie_info_layout)

        main_layout.addLayout(info_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(back_button)

        self.setLayout(main_layout)
        self.set_gradient_background()

    def fetch_movie_info(self, movie_name):
        """Fetch movie details from the server."""
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
        """Setup poster display."""
        poster_frame = QFrame()
        poster_layout = QVBoxLayout(poster_frame)
        poster_label = QLabel("Постер:")
        poster_layout.addWidget(poster_label)

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
        poster_item = QGraphicsPixmapItem(poster_pixmap.scaled(140, 190, Qt.IgnoreAspectRatio ,Qt.SmoothTransformation))
        poster_view.setRenderHint(QPainter.Antialiasing)
        poster_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        poster_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        poster_scene.addItem(poster_item)
        poster_view.setScene(poster_scene)
        poster_view.setFixedSize(140, 190)

        poster_layout.addWidget(poster_view)

        return poster_frame

    def create_placeholder_pixmap(self):
        """Create a placeholder pixmap for missing posters."""
        pixmap = QPixmap(100, 140)
        pixmap.fill(Qt.gray)
        return pixmap

    def create_star_rating(self):
        """Create a star rating layout."""
        star_label = QLabel("оценка")
        star_rating_layout = QHBoxLayout()
        self.star_buttons = QButtonGroup(self)

        for i in range(5):
            star_button = QPushButton("☆")
            star_button.setStyleSheet("font-size: 16px; color: gray; border: none;")
            star_button.setCheckable(True)
            star_button.setMaximumSize(20, 20)
            star_button.clicked.connect(self.update_star_rating)
            self.star_buttons.addButton(star_button, i + 1)
            star_rating_layout.addWidget(star_button)

        star_rating_layout.addWidget(star_label)
        star_rating_layout.addStretch()
        return star_rating_layout

    def create_schedule_table(self, clients_info):
        """Create a table to display client information."""
        table = QTableWidget()
        table.setRowCount(len(clients_info))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Имя", "Время"])

        for i, (name, times) in enumerate(clients_info.items()):
            table.setItem(i, 0, QTableWidgetItem(name))
            table.setItem(i, 1, QTableWidgetItem(", ".join(times)))
        table.resizeColumnsToContents()
        return table

    def set_gradient_background(self):
        """Set a diagonal gradient background."""
        gradient = QLinearGradient(self.width(), self.height(), 0, 0)
        gradient.setColorAt(1.0, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.5, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.0, QColor(85, 85, 85, 50))

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def update_star_rating(self):
        """Update the star rating based on user interaction."""
        selected_rating = self.star_buttons.checkedId()
        for i, button in enumerate(self.star_buttons.buttons()):
            if i + 1 <= selected_rating:
                button.setText("★")
                button.setStyleSheet("font-size: 16px; color: gold; border: none;")
            else:
                button.setText("☆")
                button.setStyleSheet("font-size: 16px; color: gray; border: none;")
