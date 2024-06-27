from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import sys, time, threading

from modules.GlobalVariable import APP_ICON, CLOSE_ICON, MINIMIZE_ICON, FOLDER_ICON, MINI_WINDOW_ICON
from modules.GlobalVariable import CSS
from modules.SimpleModules import WindowTitleBar, Button
from modules.ButtonInterface import ButtonInterface
from modules.PlaylistTable import PlaylistTable
from modules.QueuePlaylist import QueuePlaylist

# from modules.MiniWindow import MiniWindow
# from modules.WarningWindow import WarningWindow

class MainWindow(QMainWindow):
    def __init__(self, title: str):
        super().__init__()
        self._icon: QPixmap = APP_ICON
        self._title: str = title
        self._mustCheckAudioOut: bool = True
        # self.playlist: list[str] = []
        self.queue: list[int] = []

        # self.nowPlaying: int = 1
        # self.playbackState: bool = False
        # self.repeatTrack: bool = False
        # self.randomEnabled: bool = False
        # self.listOfTracks: list[int] = []

        self.setWindowIcon(QIcon(self._icon))
        self.setWindowTitle(self._title)
        self.setStyleSheet(CSS)
        self.setObjectName("MainWindow")
        self.setFixedSize(960, 560)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        windowHat = WindowTitleBar(self, self._icon, self._title, "dark-comp")
        self._buttonInterface = ButtonInterface(self, 1, self.height()-111, self.width()-2, 110)
        self._playlistTable = PlaylistTable(self, 1, windowHat.height(), ((self.width()-2) * 80) // 100, self.height()-(windowHat.height()+self._buttonInterface.height()))
        self._queueTable = QueuePlaylist(self, self._playlistTable.width()+1, windowHat.height(), ((self.width()-2) * 20) // 100, self.height()-(windowHat.height()+self._buttonInterface.height()))

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
        self.checkAudioOutThread = threading.Thread(target=self._checkAudioOut)

    def closeEvent(self, event) -> None:
        self._mustCheckAudioOut = False
        self.close()

    def _checkAudioOut(self) -> None:
        while self._mustCheckAudioOut:
            if self._mediaPlayer.audioOutput() != None:
                if self._mediaPlayer.audioOutput().device() != QAudioOutput().device():
                    self._audioOutput = QAudioOutput()
                    # self._audioOutput.setVolume(self._buttonInterface.sliderVolume.value() / 100)
                    self._mediaPlayer.setAudioOutput(self._audioOutput)
            else:
                self._audioOutput = QAudioOutput()
                # self._audioOutput.setVolume(self._buttonInterface.sliderVolume.value() / 100)
                self._mediaPlayer.setAudioOutput(self._audioOutput)
            time.sleep(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow("MP3 player")
    window.show()
    window.checkAudioOutThread.start()
    sys.exit(app.exec())

# pyinstaller -F -w -i "images/app.ico" -n "Media player" main.py