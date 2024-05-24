from PyQt6.QtWidgets import QApplication, QMainWindow, QSlider, QFileDialog
from PyQt6.QtCore import Qt, QUrl, QSize
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import sys, time

from modules.GlobalVariable import *
from modules.SimpleModules import WindowTitleBar, Button, LineEntry

from modules.PlaylistTable import PlaylistTable

class MainWindow(QMainWindow):
    def __init__(self, title: str):
        super().__init__()
        self.icon: QPixmap = APP_ICON
        self.title: str = title
        self.nowPlaying: int = 1
        self.playbackState: bool = False

        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle(self.title)
        self.setStyleSheet(CSS)
        self.setObjectName("MainWindow")
        self.setFixedSize(720, 560)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        windowHat = WindowTitleBar(self)
        btn_close = Button(self, CLOSE_ICON, self.width()-30, 0, 30, 30, "btn_red_transp", self.closeEvent)
        btn_close.setToolTip("Закрыть окно")
        btn_showMinimize = Button(self, MINIMIZE_ICON, self.width()-60, 0, 30, 30, "btn_orange_transp", self.showMinimized)
        btn_showMinimize.setToolTip("Свернуть окно")

        self.playlist = PlaylistTable(self, 1, windowHat.height(), self.width()-2, self.height()-140)

        self.__btnPlay = Button(self, PLAY_ICON, 10, self.playlist.pos().y()+self.playlist.height()+10, 125, 50, "btn_orange", self.changePlaybackState)
        self.__btnPlay.setIconSize(QSize(30,30))
        self.__btnPlay.setShortcut(Qt.Key.Key_Space)
        self.__btnPlay.setToolTip("Проиграть")
        btnPrevious = Button(self, PREVIOUS_ICON, 10, self.__btnPlay.pos().y()+self.__btnPlay.height()+10, 60, 30, "btn_orange", self.previousTrack)
        btnPrevious.setShortcut(Qt.Key.Key_Left)
        btnPrevious.setToolTip("Предыдущий трэк")
        btnNext = Button(self, NEXT_ICON, btnPrevious.pos().x()+btnPrevious.width()+5, self.__btnPlay.pos().y()+self.__btnPlay.height()+10, 60, 30, "btn_orange", self.nextTrack)
        btnNext.setShortcut(Qt.Key.Key_Right)
        btnNext.setToolTip("Следующий трэк")

        self.__mediaPlayer = QMediaPlayer()
        self.__audioOutput = QAudioOutput()
        self.__audioOutput.setVolume(0.5)
        self.__mediaPlayer.setAudioOutput(self.__audioOutput)
        self.__mediaPlayer.durationChanged.connect(lambda d: [self.__sliderDuration.setRange(0, d)])
        self.__mediaPlayer.positionChanged.connect(self.changeTimecode)
        self.__mediaPlayer.mediaStatusChanged.connect(self.mediaStatusChanged)

        self.__sliderDuration = QSlider(Qt.Orientation.Horizontal, self)
        self.__sliderDuration.move(btnNext.pos().x() + btnNext.width() + 10, btnNext.pos().y() + 8)
        self.__sliderDuration.setFixedSize(self.width() - (btnNext.pos().x() + btnNext.width() + 10) - 110, 15)
        self.__sliderDuration.sliderPressed.connect(self.__mediaPlayer.stop)
        self.__sliderDuration.sliderReleased.connect(self.sliderReleased)
        self.__sliderDuration.valueChanged.connect(self.changeTimecode)
        
        self.__entryDuration = LineEntry(self, self.__sliderDuration.pos().x()+self.__sliderDuration.width()+10, btnNext.pos().y(), 90, 30, "0:00", True, "entry")
        self.__entryDuration.setText("0:00")

    def closeEvent(self, event) -> None:
        self.close()

    def changePlaybackState(self) -> None:
        match self.__mediaPlayer.playbackState():
            case QMediaPlayer.PlaybackState.PlayingState:
                self.pause()
            case QMediaPlayer.PlaybackState.StoppedState:
                self.changeMedia(self.nowPlaying)
                self.play()
            case QMediaPlayer.PlaybackState.PausedState:
                self.play()

    def previousTrack(self) -> None:
        if self.__mediaPlayer.position() < 5000:
            if self.nowPlaying <= 1: self.changeMedia(len(self.playlist.playlist))
            else:
                self.changeMedia(self.nowPlaying-1)
                if self.playbackState: self.play()
        else: self.__mediaPlayer.setPosition(0)

    def nextTrack(self) -> None:
        if self.nowPlaying >= len(self.playlist.playlist): self.changeMedia(1)
        else:
            self.changeMedia(self.nowPlaying+1)
            if self.playbackState: self.play()

    def changeTimecode(self, d: int) -> None:
        m = d // 1000 // 60
        s = d // 1000 % 60
        self.__entryDuration.setText(f'{m:>1}:{s:0>2}') 
        self.__sliderDuration.setValue(d)

    def mediaStatusChanged(self, status: QMediaPlayer.MediaStatus) -> None:
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.nextTrack()

    def sliderReleased(self) -> None:
        self.__mediaPlayer.stop()
        self.__mediaPlayer.setPosition(self.__sliderDuration.value())
        if self.playbackState: self.play()

    def changeMedia(self, musicID: int) -> None:
        newMedia = QUrl.fromLocalFile(Rf"{self.playlist.playlist[musicID]}")
        self.__mediaPlayer.stop()
        time.sleep(0.5)
        self.__mediaPlayer.setSource(newMedia)
        for i in range(self.playlist.columnCount()):
            try: self.playlist.item(self.nowPlaying-1, i).setBackground(QColor(0,0,0,0))
            except: pass
        self.nowPlaying = musicID
        for i in range(self.playlist.columnCount()):
            try: self.playlist.item(self.nowPlaying-1, i).setBackground(QColor(255,88,0,240))
            except: pass

    def play(self) -> None:
        self.__mediaPlayer.play()
        self.playbackState = True
        self.__btnPlay.setIcon(PAUSE_ICON)
        self.__btnPlay.setToolTip("Остановить")

    def pause(self) -> None:
        self.__mediaPlayer.pause()
        self.playbackState = False
        self.__btnPlay.setIcon(PLAY_ICON)
        self.__btnPlay.setToolTip("Проиграть")

    def stop(self) -> None:
        self.__mediaPlayer.stop()
        self.playbackState = False
        self.__btnPlay.setIcon(PLAY_ICON)
        self.__btnPlay.setToolTip("Проиграть")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow("Media player")
    window.show()
    window.playlist.loadPlaylistThread.start()    
    sys.exit(app.exec())