from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QMouseEvent

from modules.SimpleModules import Label, Button
from modules.GlobalVariable import *

class MainWindow(QMainWindow):
    def closeEvent(self, event) -> None: ...
    def nextTrack(self) -> None: ...
    def previousTrack(self) -> None: ...
    def changePlaybackState(self) -> None: ...

class MoveLabel(Label):
    def __init__(self, parent: QMainWindow, width: int, height: int, objectName: str, content: str | QPixmap):
        self.myParent = parent
        self.screenSize = QApplication.primaryScreen().availableGeometry()
        super().__init__(parent, 0, 0, width, height, objectName, content)

    def mousePressEvent(self, LeftButton: QMouseEvent) -> None:
        self.pos = LeftButton.pos()
        self.main_pos = self.myParent.pos()

    def mouseMoveEvent(self, LeftButton: QMouseEvent) -> None:
        self.last_pos = LeftButton.pos() - self.pos
        self.main_pos += self.last_pos
        self.myParent.move(0, self.main_pos.y())

class MiniWindow(QMainWindow):
    def __init__(self, parent: MainWindow):
        super().__init__()
        self.myParent = parent

        self.setFixedSize(30,180)
        self.move(0, 100)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(APP_ICON))
        self.setWindowTitle(self.myParent.title)
        self.setObjectName("MiniWindow")
        self.setStyleSheet(CSS)

        btn_close = Button(self, CLOSE_ICON, 0, self.height()-30, 30, 30, "btn_red_transp", self.myParent.closeEvent)
        btn_close.setToolTip("Закрыть")
        btn_showMainWindow = Button(self, FULLSCREEN_ICON, 0, self.height()-60, 30, 30, "btn_orange_transp", self.showMainWindow)
        btn_showMainWindow.setToolTip("Открыть проигрыватель")
        
        btn_nextTrack = Button(self, NEXT_ICON, 0, self.height()-90, 30, 30, "btn_orange_transp", self.myParent.nextTrack)
        btn_nextTrack.setToolTip("Следующий трэк")
        btn_nextTrack.setIconSize(QSize(20,20))
        self.btn_play = Button(self, PLAY_ICON, 0, self.height()-120, 30, 30, "btn_orange_transp", self.myParent.changePlaybackState)
        self.btn_play.setToolTip("Проиграть")
        self.btn_play.setIconSize(QSize(20,20))
        btn_previous = Button(self, PREVIOUS_ICON, 0, self.height()-150, 30, 30, "btn_orange_transp", self.myParent.previousTrack)
        btn_previous.setToolTip("Предыдущий трэк")
        btn_previous.setIconSize(QSize(20,20))

        label_6Dots = MoveLabel(self, 30, 30, "TitleBar", DOTS_ICON)

    def showMainWindow(self) -> None:
        self.hide()
        self.myParent.show()