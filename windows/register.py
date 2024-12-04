from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox, QSpacerItem, QSizePolicy,
    QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import requests

class RegistrationPage(QWidget):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle("Регистрация")
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

        # Текст "Регистрация"
        self.title_label = QLabel("Регистрация", self)
        self.title_label.setFont(QFont("Arial", 42))
        self.title_label.setStyleSheet("color: white;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Поля ввода
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Имя пользователя")
        self.username_input.setFixedSize(295, 40)
        self.username_input.setAlignment(Qt.AlignCenter)
        self.username_input.setStyleSheet("border-radius: 5px;")

        self.password_input_confirmation = QLineEdit(self)
        self.password_input_confirmation.setPlaceholderText("Подтвердить пароль")
        self.password_input_confirmation.setEchoMode(QLineEdit.Password)
        self.password_input_confirmation.setFixedSize(295, 40)
        self.password_input_confirmation.setAlignment(Qt.AlignCenter)
        self.password_input_confirmation.setStyleSheet("border-radius: 5px;")

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedSize(295, 40)
        self.password_input.setAlignment(Qt.AlignCenter)
        self.password_input.setStyleSheet("border-radius: 5px;")

        # Кнопка регистрации
        self.register_button = QPushButton("Зарегистрироваться", self)
        self.register_button.setFixedSize(295, 40)
        self.register_button.setStyleSheet(
            "background-color: #E50914; color: white; font-size: 16px; border: none; border-radius: 5px;"
        )
    
        # Капча (ссылка на реCAPTCHA, заменить на реальную капчу)
        self.recaptcha_checkbox = QCheckBox("I'm not a robot", self)
        self.recaptcha_checkbox.setStyleSheet("color: white;")

        # Обработчик нажатия кнопки регистрации
        self.register_button.clicked.connect(self.register)
        
        # Кнопка назад
        self.login_link = QLabel('<a href="#">Войти</a>', self)
        self.login_link.setStyleSheet("color: lightblue;")
        self.login_link.setAlignment(Qt.AlignCenter)

        # Компоновка элементов
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.title_label)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.password_input_confirmation)
        form_layout.addWidget(self.register_button)
        form_layout.addWidget(self.recaptcha_checkbox)
        form_layout.addWidget(self.login_link)

        # Основной компоновщик для центрирования
        main_layout = QVBoxLayout(self)
        main_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Верхний отступ
        main_layout.addLayout(form_layout)  # Центрируемая форма
        main_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Нижний отступ

        self.login_link.linkActivated.connect(self.go_back_to_login)

    def go_back_to_login(self):
        # Создаем и показываем окно авторизации
        from windows.login import LoginPage
        self.login_page = LoginPage()
        self.login_page.show()
        self.close()

    def register(self):
        if not self.recaptcha_checkbox.isChecked():
            QMessageBox.warning(self, 'Ошибка', 'Подтвердите, что вы не робот')
            return

        # Обработка регистрации
        username = self.username_input.text()
        password = self.password_input.text()
        password_confirmation = self.password_input_confirmation.text()

        # Отправка запроса на сервер Flask для регистрации
        if password != password_confirmation:
            QMessageBox.warning(self, 'Ошибка', 'Пароли не совпадают')
            return
    
        response = requests.post('http://127.0.0.1:5000/register', json={
            'username': username,
            'password': password
        })

        # Печать содержимого ответа для диагностики
        print("Server response:", response.text)

        # Обработка ответа от сервера
        try:
            response.json()
        except requests.exceptions.JSONDecodeError:
            QMessageBox.warning(self, 'Ошибка', 'Ошибка регистрации: неверный формат ответа от сервера')
            return

        if response.status_code == 200 or response.status_code == 201: 
            QMessageBox.information(self, 'Успех', 'Успешная регистрация')
            self.go_back_to_login()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Ошибка регистрации')

        # Очистка полей ввода
        self.username_input.clear()
        self.password_input.clear()
        self.password_input_confirmation.clear()