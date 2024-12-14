from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox, QSpacerItem, QSizePolicy,
    QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import requests

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle("Авторизация")
        self.setFixedSize(800, 600)

        # Фоновое изображение
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("./img/back.jpg").scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        ))
        self.background_label.setGeometry(0, 0, 800, 600)

        # Полупрозрачный затемняющий слой
        self.overlay = QLabel(self)
        self.overlay.setGeometry(0, 0, 800, 600)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")

        # Текст "Авторизация"
        self.title_label = QLabel("Авторизация", self)
        self.title_label.setFont(QFont("Arial", 42))
        self.title_label.setStyleSheet("color: white;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Поля ввода
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Имя пользователя")
        self.username_input.setFixedSize(295, 40)
        self.username_input.setAlignment(Qt.AlignCenter)
        self.username_input.setStyleSheet("border-radius: 5px;")

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedSize(295, 40)
        self.password_input.setAlignment(Qt.AlignCenter)
        self.password_input.setStyleSheet("border-radius: 5px;")

        # Кнопка входа
        self.login_button = QPushButton("Войти", self)
        self.login_button.setFixedSize(295, 40)
        self.login_button.setStyleSheet(
            "background-color: #E50914; color: white; font-size: 16px; border: none; border-radius: 5px;"
        )
        self.login_button.clicked.connect(self.login)

        # Чекбокс reCAPTCHA
        self.recaptcha_checkbox = QCheckBox("I'm not a robot", self)
        self.recaptcha_checkbox.setStyleSheet("color: white;")

        # Ссылка регистрации
        self.register_link = QLabel('<a href="#">Регистрация</a>', self)
        self.register_link.setStyleSheet("color: lightblue;")
        self.register_link.setAlignment(Qt.AlignCenter)

        # Приветственное сообщение
        self.welcome_label = QLabel("Добро пожаловать в\nEshkere movies!", self)
        self.welcome_label.setFont(QFont("Arial", 38))
        self.welcome_label.setStyleSheet("color: white;")
        self.welcome_label.setAlignment(Qt.AlignCenter)

        # Компоновка элементов
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.title_label)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_button)
        form_layout.addWidget(self.recaptcha_checkbox, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.register_link)

        # Основной компоновщик для центрирования
        main_layout = QVBoxLayout(self)
        main_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Верхний отступ
        main_layout.addLayout(form_layout)  # Центрируемая форма
        main_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Нижний отступ
        main_layout.addWidget(self.welcome_label)

        # Перемещение виджетов на передний план
        self.title_label.raise_()
        self.username_input.raise_()
        self.password_input.raise_()
        self.login_button.raise_()
        self.recaptcha_checkbox.raise_()
        self.register_link.raise_()
        self.welcome_label.raise_()

        # Сигнал для открытия окна регистрации
        self.register_link.linkActivated.connect(self.open_registration_page)

    def open_registration_page(self):
        # Создаем и показываем окно регистрации
        from windows.register import RegistrationPage
        self.registration_page = RegistrationPage()
        self.registration_page.show()
        self.close()

    def login(self):
        # Обработка логина
        username = self.username_input.text()
        password = self.password_input.text()
        # Отправка запроса на сервер Flask для логина
        response = requests.post('https://tochka2802.pythonanywhere.com/login', json={
            'username': username,
            'password': password
        })

        # Печать содержимого ответа для диагностики
        print("Server response:", response.text)

        # Обработка ответа от сервера
        try:
            response.json()
        except requests.exceptions.JSONDecodeError:
            QMessageBox.warning(self, 'Ошибка', 'Ошибка авторизации: неверный формат ответа от сервера')
            return

        if response.status_code == 200:
            self.close()
            from windows.cinemaWindow import CinemaWindow
            self.cinema_window = CinemaWindow(self.username_input.text())
            self.cinema_window.show()
            QMessageBox.information(self, 'Успех', 'Успешная авторизация')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Ошибка авторизации')
