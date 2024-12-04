import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QLineEdit, QFileDialog, QDialog, QDialogButtonBox, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QLinearGradient, QBrush, QColor, QPainter, QPalette, QFont
from PyQt5.QtCore import Qt, QRect


class UserProfile(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the initial theme to light
        self.theme = "light"

        # Set the font globally for the application
        font = QFont("Montserrat")
        QApplication.setFont(font)

        # Main window setup
        self.setWindowTitle("Профиль пользователя")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)
        self.initUI()
        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme to the application."""
        palette = self.palette()

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        if self.theme == "light":
            # Light theme gradient
            gradient.setColorAt(1.0, QColor(136, 0, 0, 35))  # Красный оттенок (нижний правый угол)
            gradient.setColorAt(0.0, QColor(85, 85, 85, 0.33))  # Серый оттенок (верхний левый угол)
            text_color = "white"
        else:
            # Dark theme gradient
            gradient.setColorAt(1.0, QColor(50, 50, 50, 180))  # Dark gray (lower right corner)
            gradient.setColorAt(0.0, QColor(70, 130, 180, 150))  # Steel blue (upper left corner)

            text_color = "white"

        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # Update styles for other elements
        self.name_label.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            font-family: 'Montserrat', sans-serif;
            color: {text_color};
        """)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()

    def initUI(self):
        # Central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Theme toggle button (moved to the right)
        self.theme_toggle_button = QPushButton("Тема", self)
        self.theme_toggle_button.setStyleSheet("""
            font-size: 14px;
            height: 30px;
            width: 100px;
            border-radius: 5px;
            background-color: red;
            color: white;
            text-align: center;
        """)
        self.theme_toggle_button.clicked.connect(self.toggle_theme)

        # Place the theme button at the top of the window (aligned to the right)
        layout.addWidget(self.theme_toggle_button, alignment=Qt.AlignRight)

        # User avatar
        self.avatar_label = QLabel(self)
        self.avatar_label.setFixedSize(200, 200)
        self.avatar_label.setStyleSheet("border: 2px solid gray; border-radius: 100px; background-color: lightgray;")
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setPixmap(QPixmap("default_avatar.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(self.avatar_label, alignment=Qt.AlignCenter)

        # Username
        self.name_label = QLabel("Имя Пользователя", self)
        layout.addWidget(self.name_label, alignment=Qt.AlignCenter)

        # Buttons layout
        button_layout = QVBoxLayout()

        button_style = """
            font-size: 16px;
            height: 30px;
            width: 200px;
            border-radius: 5px; 
            margin-bottom: 10px;
            background-color: red;
            color: white;
            border: none;
            text-align: center;
        """

        self.change_name_button = QPushButton("Сменить имя", self)
        self.change_name_button.setStyleSheet(button_style)
        self.change_name_button.clicked.connect(self.change_name)
        button_layout.addWidget(self.change_name_button, alignment=Qt.AlignCenter)

        self.change_avatar_button = QPushButton("Сменить аватарку", self)
        self.change_avatar_button.setStyleSheet(button_style)
        self.change_avatar_button.clicked.connect(self.change_avatar)
        button_layout.addWidget(self.change_avatar_button, alignment=Qt.AlignCenter)

        self.back_button = QPushButton("Назад", self)
        self.back_button.setStyleSheet(button_style)
        button_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        layout.addLayout(button_layout)

    def change_name(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Сменить имя")

        layout = QVBoxLayout(dialog)
        input_field = QLineEdit(self)
        input_field.setPlaceholderText("Введите новое имя")
        layout.addWidget(input_field)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)

        def on_accept():
            new_name = input_field.text()
            if new_name.strip():
                self.name_label.setText(new_name)
            dialog.accept()

        buttons.accepted.connect(on_accept)
        buttons.rejected.connect(dialog.reject)

        dialog.exec_()

    def change_avatar(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp)")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserProfile()
    window.show()
    sys.exit(app.exec_())
