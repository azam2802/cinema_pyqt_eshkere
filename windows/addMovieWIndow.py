from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QSizePolicy, QLabel, QFileDialog
from PyQt5.QtGui import QLinearGradient, QPalette, QBrush, QColor, QPixmap
import requests
from windows.snowflakes import SnowfallBackground

class AddMovieWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.snowfall_background = SnowfallBackground(self)

        self.setWindowTitle("Добавить фильм")
        self.setFixedSize(300, 500)

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название фильма")
        layout.addWidget(self.title_input)

        self.showtime_input = QLineEdit()
        self.showtime_input.setPlaceholderText("Время сеанса (например: 10:00)")
        layout.addWidget(self.showtime_input)

        self.cost_input = QLineEdit()
        self.cost_input.setPlaceholderText("Стоимость фильма")
        layout.addWidget(self.cost_input)

        self.image_label = QLabel("Выберите изображение")
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.image_label.setMinimumHeight(300)
        self.image_label.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0; text-align: center; color: black")
        layout.addWidget(self.image_label)

        self.image_button = QPushButton("Загрузить изображение")
        self.image_button.clicked.connect(self.upload_image)
        layout.addWidget(self.image_button)

        self.add_button = QPushButton("Добавить фильм")
        layout.addWidget(self.add_button)
        self.snowfall_background.create_snowflakes()
        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_movie)
        self.set_gradient_background()

    def set_gradient_background(self):
        gradient = QLinearGradient(self.width(), self.height(), 0, 0)
        gradient.setColorAt(1.0, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.5, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.0, QColor(85, 85, 85, 50))

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def upload_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать изображение", "", "Images (*.png *.jpg *.jpeg *.gif)", options=options)
        print(file_path)
        if file_path:
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height())
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setToolTip(file_path)

    def add_movie(self):
        title = self.title_input.text()
        showtime = [i.strip() for i in self.showtime_input.text().split(",")]
        cost = self.cost_input.text()
        image_path = self.image_label.toolTip()
        print(image_path)
        files = {"poster": open(image_path, "rb")}

        if not title or not showtime or not cost or not image_path:
            print("All fields are required")
            return

        try:
            files = {"poster": open(image_path, "rb")}
            data = {
                'title': title,
                'showtime': showtime, 
                'cost': cost
            }
            print(showtime)

            response = requests.post('https://tochka2802.pythonanywhere.com/movies/addMovie', json=data)
            print(response.status_code, "status code")
            response = requests.post('https://tochka2802.pythonanywhere.com/movies/addPoster', data={"title": data.get("title")}, files=files)
            print(response.status_code, "status code")

            if response.status_code == 200 or response.status_code == 201:
                self.accept()  
    
        except Exception as e:
            print(f"An error occurred: {e}")