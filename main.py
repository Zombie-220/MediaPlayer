from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import sys, time, threading

from modules.GlobalVariable import *
from modules.SimpleModules import WindowTitleBar, Button
from modules.PlaylistTable import PlaylistTable
from modules.MiniWindow import MiniWindow
from modules.ButtonInterface import ButtonInterface
from modules.WarningWindow import WarningWindow

class MainWindow(QMainWindow):
    def __init__(self, title: str):
        super().__init__()
        self.icon: QPixmap = APP_ICON
        self.title: str = title
        self.nowPlaying: int = 1
        self.playbackState: bool = False
        self.repeatTrack: bool = False
        self.randomEnabled: bool = False
        self.listOfTracks: list[int] = []
        self.mustCheckAudioOut: bool = True

        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle(self.title)
        self.setStyleSheet(CSS)
        self.setObjectName("MainWindow")
        self.setFixedSize(720, 560)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        windowHat = WindowTitleBar(self, self.icon, self.title, "TitleBar")
        btn_close = Button(self, CLOSE_ICON, self.width()-30, 0, 30, 30, "btn_red_transp", self.closeEvent)
        btn_close.setToolTip("Закрыть окно")
        btn_showMinimize = Button(self, MINIMIZE_ICON, self.width()-60, 0, 30, 30, "btn_orange_transp", self.showMinimized)
        btn_showMinimize.setToolTip("Свернуть окно")
        self.playlist = PlaylistTable(self, 1, windowHat.height(), self.width()-2, self.height()-140)
        btn_changeRep = Button(self, FOLDER_ICON, self.width()-120, 0, 30, 30, "btn_orange_transp", self.playlist.changeDir)
        btn_changeRep.setToolTip("Выбрать папку")
        btn_changeRep.setIconSize(QSize(20,20))
        self.btn_openMiniWindow = Button(self, MINI_WINDOW_ICON, self.width()-90, 0, 30, 30, "btn_orange_transp", self.openMiniWindow)
        self.btn_openMiniWindow.setToolTip("Открыть мини проигрыватель")
        self.btn_openMiniWindow.setIconSize(QSize(20,20))

        self.mediaPlayer = QMediaPlayer(self)
        self.__audioOutput = QAudioOutput(self)
        self.mediaPlayer.setAudioOutput(self.__audioOutput)

        self.buttonInterface = ButtonInterface(self, 0,windowHat.height()+self.playlist.height(), self.width(), self.height()-(windowHat.height()+self.playlist.height()), "label")
        self.miniWindow = MiniWindow(self)

        self.mediaPlayer.durationChanged.connect(lambda d: [self.buttonInterface.sliderDuration.setRange(0, d)])
        self.mediaPlayer.positionChanged.connect(self.buttonInterface.changeTimecode)
        self.mediaPlayer.mediaStatusChanged.connect(self.buttonInterface.mediaStatusChanged)
        self.checkAudioOutThread = threading.Thread(target=self.checkAudioOut)

        self.warningWindow = WarningWindow(self)

    def closeEvent(self, event) -> None:
        self.mustCheckAudioOut = False
        self.close()
        self.miniWindow.close()

    def checkAudioOut(self) -> None:
        while self.mustCheckAudioOut:
            if self.mediaPlayer.audioOutput() != None:
                if self.mediaPlayer.audioOutput().device() != QAudioOutput().device():
                    self.__audioOutput = QAudioOutput()
                    self.__audioOutput.setVolume(self.buttonInterface.sliderVolume.value() / 100)
                    self.mediaPlayer.setAudioOutput(self.__audioOutput)
            else:
                self.__audioOutput = QAudioOutput()
                self.__audioOutput.setVolume(self.buttonInterface.sliderVolume.value() / 100)
                self.mediaPlayer.setAudioOutput(self.__audioOutput)
            time.sleep(1)

    def openMiniWindow(self) -> None:
        self.hide()
        self.miniWindow.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow("Media player")
    window.show()
    window.playlist.loadPlaylistThread.start()
    window.checkAudioOutThread.start()
    sys.exit(app.exec())

# pyinstaller -F -w -i "images/app.ico" -n "Media player" main.py