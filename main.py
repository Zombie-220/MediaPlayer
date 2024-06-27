from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import sys, time, threading

from modules.GlobalVariable import APP_ICON, CLOSE_ICON, MINIMIZE_ICON, FOLDER_ICON, MINI_WINDOW_ICON
from modules.GlobalVariable import CSS
from modules.SimpleModules import WindowTitleBar, Button
from modules.ButtonInterface import ButtonInterface

# from modules.PlaylistTable import PlaylistTable
# from modules.MiniWindow import MiniWindow
# from modules.WarningWindow import WarningWindow
# from modules.QueuePlaylist import QueuePlaylist

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
        self.setFixedSize(960, 560)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        windowHat = WindowTitleBar(self, self.icon, self.title, "dark-comp")
        self._buttonInterface = ButtonInterface(self, 1, self.height()-301, self.width()-2, 300, "transp-widget")

        btn_close = Button(self, CLOSE_ICON, self.width()-30, 0, 30, 30, "btn_red_transp", self.closeEvent)
        btn_close.setToolTip("Закрыть окно")
        btn_showMinimize = Button(self, MINIMIZE_ICON, self.width()-60, 0, 30, 30, "btn_orange_transp", self.showMinimized)
        btn_showMinimize.setToolTip("Свернуть окно")
        # btn_changeRep = Button(self, FOLDER_ICON, self.width()-120, 0, 30, 30, "btn_orange_transp", self._playlist.changeDir)
        btn_changeRep = Button(self, FOLDER_ICON, self.width()-120, 0, 30, 30, "btn_orange_transp")
        btn_changeRep.setToolTip("Выбрать папку")
        btn_changeRep.setIconSize(QSize(20,20))
        # self._btn_openMiniWindow = Button(self, MINI_WINDOW_ICON, self.width()-90, 0, 30, 30, "btn_orange_transp", self.openMiniWindow)
        self._btn_openMiniWindow = Button(self, MINI_WINDOW_ICON, self.width()-90, 0, 30, 30, "btn_orange_transp")
        self._btn_openMiniWindow.setToolTip("Открыть мини проигрыватель")
        self._btn_openMiniWindow.setIconSize(QSize(20,20))

        self._mediaPlayer = QMediaPlayer(self)
        self._audioOutput = QAudioOutput(self)
        self._mediaPlayer.setAudioOutput(self._audioOutput)

        # self._mediaPlayer.durationChanged.connect(lambda d: [self._buttonInterface.sliderDuration.setRange(0, d)])
        # self._mediaPlayer.positionChanged.connect(self._buttonInterface.changeTimecode)
        # self._mediaPlayer.mediaStatusChanged.connect(self._buttonInterface.mediaStatusChanged)
        self.checkAudioOutThread = threading.Thread(target=self.checkAudioOut)

    def closeEvent(self, event) -> None:
        self.mustCheckAudioOut = False
        self.close()

    def checkAudioOut(self) -> None:
        while self.mustCheckAudioOut:
            if self._mediaPlayer.audioOutput() != None:
                if self._mediaPlayer.audioOutput().device() != QAudioOutput().device():
                    self._audioOutput = QAudioOutput()
                    self._audioOutput.setVolume(self._buttonInterface.sliderVolume.value() / 100)
                    self._mediaPlayer.setAudioOutput(self._audioOutput)
            else:
                self._audioOutput = QAudioOutput()
                self._audioOutput.setVolume(self._buttonInterface.sliderVolume.value() / 100)
                self._mediaPlayer.setAudioOutput(self._audioOutput)
            time.sleep(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow("MP3 player")
    window.show()
    window.checkAudioOutThread.start()
    sys.exit(app.exec())

# pyinstaller -F -w -i "images/app.ico" -n "Media player" main.py