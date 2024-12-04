from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
import requests

class MovieInfoWindow(QWidget):
    def __init__(self, movie_name, time, movie_info):
        super().__init__()
        self.setWindowTitle("Информация о фильме")
        self.resize(500, 300)

        response = requests.post('http://127.0.0.1:5000/movies/getMovieInfo', json={'title': movie_name})
        if response.status_code == 200:
            clients_info = response.json()
        else:
            clients_info = {}

        # Movie details
        name_label = QLabel(f"Название: {movie_name}")
        session_count_label = QLabel(f"Сеансы: {len(movie_info['showTime'])}")
        seats_label = QLabel(f"Места: {movie_info['seats']}")

        # Schedule table
        self.table = QTableWidget()
        self.table.setRowCount(len(clients_info))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Имя", "Время"])

        # Populate table
        for i, name in enumerate(clients_info):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(", ".join(clients_info[name])))
        self.table.resizeColumnsToContents()

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