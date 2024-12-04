from PyQt5.QtWidgets import QApplication
from windows.login import LoginPage
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())