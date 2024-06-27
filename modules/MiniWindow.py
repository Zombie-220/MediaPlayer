from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent

from modules.SimpleModules import Label, Button
from modules.GlobalVariable import APP_ICON, CSS, CLOSE_ICON, FULLSCREEN_ICON, NEXT_ICON, PLAY_ICON,PREVIOUS_ICON, DOTS_ICON

from MainWindowHeader import MainWindow

class MoveLabel(Label):
    def __init__(self, parent: MainWindow, width: int, height: int, objectName: str, content: str | QPixmap):
        self._parent = parent
        self._screenSize = QApplication.primaryScreen().availableGeometry()
        super().__init__(parent, 0, 0, width, height, objectName, content)

    def mousePressEvent(self, LeftButton: QMouseEvent) -> None:
        self._x_pos = LeftButton.pos().x()
        self._y_pos = LeftButton.pos().y()
        self._main_pos = self._parent.pos()

    def mouseMoveEvent(self, LeftButton: QMouseEvent) -> None:
        if self._parent.pos().x() == 0:
            if LeftButton.pos().x() <= self._screenSize.width() // 2: self._last_pos = QPoint(0, LeftButton.pos().y() - self._y_pos)
            else: self._last_pos = QPoint(self._screenSize.width() - self._parent.width(), LeftButton.pos().y() - self._x_pos)
        elif self._parent.pos().x() == self._screenSize.width() - self._parent.width():
            if -(LeftButton.pos().x()) <= self._screenSize.width() // 2: self._last_pos = QPoint(0, LeftButton.pos().y() - self._y_pos)
            else: self._last_pos = QPoint(-(self._screenSize.width() - self._parent.width()), LeftButton.pos().y() - self._x_pos)
        self._main_pos += self._last_pos
        self._parent.move(self._main_pos)

class MiniWindow(QMainWindow):
    def __init__(self, parent: MainWindow):
        super().__init__()
        self._parent = parent
        self._screenSize = QApplication.primaryScreen().availableGeometry()

        self.setFixedSize(30,180)
        self.move(0, self._screenSize.height()//2 - self.height()//2)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(APP_ICON))
        self.setWindowTitle(self._parent.title)
        self.setObjectName("MiniWindow")
        self.setStyleSheet(CSS)

        btn_close = Button(self, CLOSE_ICON, 0, self.height()-30, 30, 30, "btn_red_transp", self._parent.closeEvent)
        btn_close.setToolTip("Закрыть")
        btn_showMainWindow = Button(self, FULLSCREEN_ICON, 0, self.height()-60, 30, 30, "btn_orange_transp", self.showMainWindow)
        btn_showMainWindow.setToolTip("Открыть проигрыватель")
        
        btn_nextTrack = Button(self, NEXT_ICON, 0, self.height()-90, 30, 30, "btn_orange_transp", self._parent.nextTrack)
        btn_nextTrack.setToolTip("Следующий трэк")
        btn_nextTrack.setIconSize(QSize(20,20))
        self.btn_play = Button(self, PLAY_ICON, 0, self.height()-120, 30, 30, "btn_orange_transp", self._parent.changePlaybackState)
        self.btn_play.setToolTip("Проиграть")
        self.btn_play.setIconSize(QSize(20,20))
        btn_previous = Button(self, PREVIOUS_ICON, 0, self.height()-150, 30, 30, "btn_orange_transp", self._parent.previousTrack)
        btn_previous.setToolTip("Предыдущий трэк")
        btn_previous.setIconSize(QSize(20,20))

        label_6Dots = MoveLabel(self, 30, 30, "TitleBar", DOTS_ICON)

    def showMainWindow(self) -> None:
        self.hide()
        self._parent.show()

    def closeEvent(self, event) -> None:
        self._parent.closeEvent(event)