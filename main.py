from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import sys

from modules.GlobalVariable import *
from modules.SimpleModules import WindowTitleBar, Button

class MainWindow(QMainWindow):
    def __init__(self, title: str):
        super().__init__()
        self.icon = APP_ICON
        self.title = title

        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle(self.title)
        self.setStyleSheet(CSS)
        self.setObjectName("MainWindow")
        self.setFixedSize(720, 560)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        windowHat = WindowTitleBar(self)
        btn_close = Button(self, CLOSE_ICON, self.width()-30, 0, 30, 30, "btn_red_transp", self.closeEvent)
        btn_showMinimize = Button(self, MINIMIZE_ICON, self.width()-60, 0, 30, 30, "btn_orange_transp", self.showMinimized)

    def closeEvent(self, event) -> None:
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow("Media player")
    window.show()
    sys.exit(app.exec())