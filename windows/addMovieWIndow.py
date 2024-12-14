from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QLinearGradient, QPalette, QBrush, QColor, QPixmap
import requests

class AddMovieWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить фильм")
        self.setFixedSize(300, 400)

        # Create layout and widgets
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
        self.image_label.setFixedSize(200, 200)
        self.image_label.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        layout.addWidget(self.image_label)

        self.image_button = QPushButton("Загрузить изображение")
        self.image_button.clicked.connect(self.upload_image)
        layout.addWidget(self.image_button)

        self.add_button = QPushButton("Добавить фильм")
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        # Connect signals
        self.add_button.clicked.connect(self.add_movie)
        self.set_gradient_background()

    def set_gradient_background(self):
        """Set a diagonal gradient background."""
        gradient = QLinearGradient(self.width(), self.height(), 0, 0)
        gradient.setColorAt(1.0, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.5, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.0, QColor(85, 85, 85, 50))

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def upload_image(self):
        """Open file dialog to select an image."""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать изображение", "", "Images (*.png *.jpg *.jpeg *.gif)", options=options)
        print(file_path)
        if file_path:
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height())
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setToolTip(file_path)  # Store the file path as a tooltip

    def add_movie(self):
        title = self.title_input.text()
        showtime = self.showtime_input.text().split(",")
        showtime = [str(i).strip() for i in showtime]
        cost = self.cost_input.text()
        image_path = self.image_label.toolTip()
        print(image_path)
        files = {"poster": open(image_path, "rb")}


        if not title or not showtime or not cost or not image_path:
            print("All fields are required")
            return

        data = {
            'title': title,
            'showtime': [showtime],
            'cost': cost
        }

        # Send POST request to add movie
        response = requests.post('https://tochka2802.pythonanywhere.com/movies/addMovie', data=data, files=files)
        print(response.status_code, "status code")
        if response.status_code == 201:
            print("Movie added successfully")
            self.accept()  # Close the add movie window after successful add
        else:
            print(f"Error adding movie: {response.json().get('message')}")
