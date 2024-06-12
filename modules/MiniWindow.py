from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent

from modules.SimpleModules import Label, Button
from modules.GlobalVariable import APP_ICON, CSS, CLOSE_ICON, FULLSCREEN_ICON, NEXT_ICON, PLAY_ICON,PREVIOUS_ICON, DOTS_ICON

class MainWindow(QMainWindow):
    def nextTrack(self) -> None: ...
    def changePlaybackState(self) -> None: ...
    def previousTrack(self) -> None: ...

class MoveLabel(Label):
    def __init__(self, parent: QMainWindow, width: int, height: int, objectName: str, content: str | QPixmap):
        self.myParent = parent
        self.__screenSize = QApplication.primaryScreen().availableGeometry()
        super().__init__(parent, 0, 0, width, height, objectName, content)

    def mousePressEvent(self, LeftButton: QMouseEvent) -> None:
        self.__x_pos = LeftButton.pos().x()
        self.__y_pos = LeftButton.pos().y()
        self.__main_pos = self.myParent.pos()

    def mouseMoveEvent(self, LeftButton: QMouseEvent) -> None:
        if self.myParent.pos().x() == 0:
            if LeftButton.pos().x() <= self.__screenSize.width() // 2: self.__last_pos = QPoint(0, LeftButton.pos().y() - self.__y_pos)
            else: self.__last_pos = QPoint(self.__screenSize.width() - self.myParent.width(), LeftButton.pos().y() - self.__x_pos)
        elif self.myParent.pos().x() == self.__screenSize.width() - self.myParent.width():
            if -(LeftButton.pos().x()) <= self.__screenSize.width() // 2: self.__last_pos = QPoint(0, LeftButton.pos().y() - self.__y_pos)
            else: self.__last_pos = QPoint(-(self.__screenSize.width() - self.myParent.width()), LeftButton.pos().y() - self.__x_pos)
        self.__main_pos += self.__last_pos
        self.myParent.move(self.__main_pos)

class MiniWindow(QMainWindow):
    def __init__(self, parent: MainWindow):
        super().__init__()
        self.myParent = parent
        self.__screenSize = QApplication.primaryScreen().availableGeometry()

        self.setFixedSize(30,180)
        self.move(0, self.__screenSize.height()//2 - self.height()//2)
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