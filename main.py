from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QUrl, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import sys, time

from modules.GlobalVariable import *
from modules.SimpleModules import WindowTitleBar, Button

from modules.PlaylistTable import PlaylistTable

class MainWindow(QMainWindow):
    def __init__(self, title: str):
        super().__init__()
        self.icon: QPixmap = APP_ICON
        self.title: str = title
        self.nowPlaying: int = 0

        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle(self.title)
        self.setStyleSheet(CSS)
        self.setObjectName("MainWindow")
        self.setFixedSize(720, 560)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        windowHat = WindowTitleBar(self)
        btn_close = Button(self, CLOSE_ICON, self.width()-30, 0, 30, 30, "btn_red_transp", self.closeEvent)
        btn_showMinimize = Button(self, MINIMIZE_ICON, self.width()-60, 0, 30, 30, "btn_orange_transp", self.showMinimized)

        self.playlist = PlaylistTable(self, 1, windowHat.height(), self.width()-2, self.height()-140)

        self.__btnPlay = Button(self, PLAY_ICON, 10, self.playlist.pos().y()+self.playlist.height()+10, 125, 50, "btn_orange", self.changePlaybackState)
        self.__btnPlay.setIconSize(QSize(30,30))
        btnPrevious = Button(self, PREVIOUS_ICON, 10, self.__btnPlay.pos().y()+self.__btnPlay.height()+10, 60, 30, "btn_orange", self.previousTrack)
        btnNext = Button(self, NEXT_ICON, btnPrevious.pos().x()+btnPrevious.width()+5, self.__btnPlay.pos().y()+self.__btnPlay.height()+10, 60, 30, "btn_orange", self.nextTrack)

        self.__mediaPlayer = QMediaPlayer()
        self.__audioOutput = QAudioOutput()
        self.__audioOutput.setVolume(0.5)
        self.__mediaPlayer.setAudioOutput(self.__audioOutput)

    def closeEvent(self, event) -> None:
        self.close()

    def changeMedia(self, musicID: int) -> None:
        newMedia = QUrl.fromLocalFile(Rf"{self.playlist.playlist[musicID]}")
        self.__mediaPlayer.stop()
        time.sleep(0.5)
        self.__mediaPlayer.setSource(newMedia)
        self.nowPlaying = musicID
        self.__mediaPlayer.play()
        self.__btnPlay.setIcon(PAUSE_ICON)
        print(self.playlist.playlist[self.nowPlaying])

    def previousTrack(self):
        if self.nowPlaying <= 1: self.changeMedia(len(self.playlist.playlist))
        else: self.changeMedia(self.nowPlaying-1)

    def nextTrack(self):
        if self.nowPlaying >= len(self.playlist.playlist): self.changeMedia(1)
        else: self.changeMedia(self.nowPlaying+1)

    def changePlaybackState(self):
        match self.__mediaPlayer.playbackState():
            case QMediaPlayer.PlaybackState.PlayingState:
                self.__mediaPlayer.pause()
                self.__btnPlay.setIcon(PLAY_ICON)
            case QMediaPlayer.PlaybackState.StoppedState:
                self.changeMedia(1)
                self.__btnPlay.setIcon(PAUSE_ICON)
            case QMediaPlayer.PlaybackState.PausedState:
                self.__mediaPlayer.play()
                self.__btnPlay.setIcon(PAUSE_ICON)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow("Media player")
    window.show()
    window.playlist.loadPlaylistThread.start()
    sys.exit(app.exec())