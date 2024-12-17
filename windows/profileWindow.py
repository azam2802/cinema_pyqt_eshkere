from PyQt5.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QFileDialog,
    QDialog, QWidget, QPushButton
)
from PyQt5.QtGui import QPixmap, QLinearGradient, QBrush, QColor, QPainter, QPalette, QFont, QPen, QRegion
from PyQt5.QtCore import Qt, QRect
import requests 
from windows.snowflakes import SnowfallBackground

class UserProfile(QDialog):
    def __init__(self, username, avatar_pixmap=None, parent=None):
        super().__init__(parent)
        self.snowfall_background = SnowfallBackground(self)
        self.snowfall_background.create_snowflakes()
        self.theme = "light"
        self.avatar_pixmap = avatar_pixmap
        self.username = username
        font = QFont("Montserrat")
        QApplication.setFont(font)

        self.setWindowTitle("Профиль пользователя")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)
        self.initUI()

    def set_gradient_background(self):
        gradient = QLinearGradient(self.width(), self.height(), 0, 0)
        gradient.setColorAt(1.0, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.5, QColor(136, 0, 0, 100))
        gradient.setColorAt(0.0, QColor(85, 85, 85, 50))

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)


    def create_styled_button(self, text):
        button = QPushButton(text)
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

    def initUI(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        self.setLayout(layout)
        self.set_gradient_background()
        self.avatar_label = QLabel(self)
        self.avatar_label.setFixedSize(200, 200)
        self.avatar_label.setStyleSheet("""
            QLabel {
                border: 2px solid gray;
                border-radius: 100px;
                background-color: transparent;
            }
        """)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        
        if self.avatar_pixmap:
            size = 200
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
            
            scaled_avatar = self.avatar_pixmap.scaled(
                size, size,
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            
            result = QPixmap(size, size)
            result.fill(Qt.transparent)
            
            painter = QPainter(result)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setCompositionMode(QPainter.CompositionMode_Source)
            
            painter.setClipRegion(QRegion(mask.mask()))
            painter.drawPixmap(0, 0, scaled_avatar)
            painter.end()
            
            self.avatar_label.setPixmap(result)
        else:
            default_pixmap = QPixmap("default_avatar.png")
            if not default_pixmap.isNull():
                scaled_default = default_pixmap.scaled(
                    220,220,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.avatar_label.setPixmap(scaled_default)
            else:
                self.avatar_label.setText("No Avatar")
        
        layout.addWidget(self.avatar_label, alignment=Qt.AlignCenter)


        self.name_label = QLabel(self.username, self)
        self.name_label.setFont(QFont("Arial", 40))
        self.name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignCenter)

        button_layout = QVBoxLayout()
        self.change_avatar_button = self.create_styled_button("Сменить аватарку")
        self.change_avatar_button.setFixedSize(295, 35)
        self.change_avatar_button.clicked.connect(self.change_avatar)
        button_layout.addWidget(self.change_avatar_button, alignment=Qt.AlignCenter)

        self.logout_button = self.create_styled_button("Выйти из аккаунта")
        self.logout_button.setFixedSize(295, 35)
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
        """)
        self.logout_button.clicked.connect(self.logout)
        button_layout.addWidget(self.logout_button, alignment=Qt.AlignCenter)

        self.back_button = self.create_styled_button("Назад")
        self.back_button.setFixedSize(295, 35)
        self.back_button.clicked.connect(self.close)
        button_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        layout.addLayout(button_layout)

   

    def change_avatar(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        print(file_path)
        if file_path:
            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                print("Failed to load image!")
                return
            size = min(pixmap.width(), pixmap.height())
            cropped_pixmap = pixmap.copy((pixmap.width() - size) // 2, (pixmap.height() - size) // 2, size, size)
            rounded_pixmap = QPixmap(size, size)
            rounded_pixmap.fill(Qt.transparent)
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(cropped_pixmap))
            painter.drawEllipse(QRect(0, 0, size, size))
            painter.end()
            self.avatar_label.setPixmap(rounded_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))


            try:
                files = {"avatar": open(file_path, "rb")}
                data = {
                    'username': self.username
                }

                response = requests.post('https://tochka2802.pythonanywhere.com/users/setAvatar', data=data, files=files)
                print(response.status_code, "status code")

                if response.status_code == 200 or response.status_code == 201:
                    self.accept()  
                        
            except Exception as e:
                print(f"An error occurred: {e}")

    def logout(self):
        for widget in QApplication.topLevelWidgets():
            widget.close()
        
        from windows.login import LoginPage
        
        login_window = LoginPage()
        login_window.show()