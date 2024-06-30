from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import sys, os, time
import threading
import sqlite3
import random

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
        self._nowPlaying: int = 0
        self._playlist: list[str] = []
        self._playbackState: bool = False
        self._randomEnabled: bool = False
        self._alreadyUsedTracks: list[int] = []

        # self.queue: list[int] = []

        # self.repeatTrack: bool = False
        # self.randomEnabled: bool = False

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
        btn_changeRep = Button(self, FOLDER_ICON, self.width()-120, 0, 30, 30, "btn_orange_transp", self._changeDir)
        btn_changeRep.setToolTip("Выбрать папку")
        btn_changeRep.setIconSize(QSize(20,20))
        # self._btn_openMiniWindow = Button(self, MINI_WINDOW_ICON, self.width()-90, 0, 30, 30, "btn_orange_transp", self.openMiniWindow)
        self._btn_openMiniWindow = Button(self, MINI_WINDOW_ICON, self.width()-90, 0, 30, 30, "btn_orange_transp")
        self._btn_openMiniWindow.setToolTip("Открыть мини проигрыватель")
        self._btn_openMiniWindow.setIconSize(QSize(20,20))

        self._mediaPlayer = QMediaPlayer(self)
        self._audioOutput = QAudioOutput(self)
        self._audioOutput.setVolume(0.2)
        self._mediaPlayer.setAudioOutput(self._audioOutput)

        # self._mediaPlayer.durationChanged.connect(lambda d: [self._buttonInterface.sliderDuration.setRange(0, d)])
        # self._mediaPlayer.positionChanged.connect(self._buttonInterface.changeTimecode)
        # self._mediaPlayer.mediaStatusChanged.connect(self._buttonInterface.mediaStatusChanged)
        self.checkAudioOutThread = threading.Thread(target=self._checkAudioOut)
        self._path = self._getPath()
        self.loadPlaylistThread = threading.Thread(target=lambda: [self._loadPlaylist(self._path)])

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

    def _loadPlaylist(self, path: str) -> None:
        self._playlistTable.clearTable()
        self._nowPlaying = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.mp3'):
                    self._playlist.append(f"{path}\\{file}")
                    self._playlistTable.addTableItem(path, file)
            break
        if self._playlist == []: self._buttonInterface.setDisabled(True)
        else: self._buttonInterface.setDisabled(False)

    def _changeDir(self) -> None:
        # self.myParent.buttonInterface.stop()
        newPath = QFileDialog.getExistingDirectory(directory=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        dirHasMP3 = False
        for root, dirs, files in os.walk(newPath):
            for file in files:
                if file.endswith('.mp3'):
                    dirHasMP3 = True
                    break
            break
        if not dirHasMP3:
            # self.warningWindow.show()
            self.setDisabled(True)
        else:
            self._path = newPath
            self.loadPlaylistThread = threading.Thread(target=lambda: [self._loadPlaylist(self._path)])
            self.loadPlaylistThread.start()

            connect = sqlite3.connect("database.db")
            cursor = connect.cursor()
            cursor.execute("UPDATE pathToDir SET path=?", (self._path,))
            connect.commit()
            connect.close()

    def _getPath(self) -> str:
        connect = sqlite3.connect("database.db")
        cursor = connect.cursor()
        if cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pathToDir'").fetchone() == None:
            cursor.execute("CREATE TABLE pathToDir (id INTEGER PRIMARY KEY, path TEXT NOT NULL)")
            newPath = QFileDialog.getExistingDirectory(directory=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
            cursor.execute("INSERT INTO pathToDir (path) VALUES (?)", (newPath,))
            connect.commit()
            path = newPath
        else:
            path = cursor.execute("SELECT path FROM pathToDir").fetchone()[0]
        connect.close()
        return path
    
    def changeMedia(self, musicID: int) -> None:
        newMedia = QUrl.fromLocalFile(Rf"{self._playlist[musicID]}")
        self._mediaPlayer.stop()
        time.sleep(0.5)
        self._mediaPlayer.setSource(newMedia)

        self._playlistTable.changeMedia(self._nowPlaying, musicID)
        self._buttonInterface.changeMedia(self._playlist[musicID])

        self._nowPlaying = musicID

    def play(self) -> None:
        self._mediaPlayer.play()
        self._playbackState = True
        self._buttonInterface.changePlayButton(self._playbackState)

    def stop(self) -> None:
        self._mediaPlayer.stop()
        self._playbackState = False
        self._buttonInterface.changePlayButton(self._playbackState)

    def pause(self) -> None:
        self._mediaPlayer.pause()
        self._playbackState = False
        self._buttonInterface.changePlayButton(self._playbackState)

    def changePlaybackState(self) -> None:
        match self._mediaPlayer.playbackState():
            case QMediaPlayer.PlaybackState.StoppedState:
                if self._randomEnabled:
                    if len(self._playlist) == len(self._alreadyUsedTracks): self._alreadyUsedTracks = []
                    nextTrack = random.randint(0, len(self._playlist))
                    while nextTrack in self._alreadyUsedTracks: nextTrack = random.randint(0, len(self._playlist))
                else: nextTrack = self._nowPlaying
                self.changeMedia(nextTrack)
                self.play()
            case QMediaPlayer.PlaybackState.PlayingState: self.pause()
            case QMediaPlayer.PlaybackState.PausedState: self.play()

    def changeRandom(self) -> None:
        self._randomEnabled = not self._randomEnabled
        self._buttonInterface.changeRandomButton(self._randomEnabled)

    def previousTrack(self) -> None:
        if self._mediaPlayer.position() > 5000: self._mediaPlayer.setPosition(0)
        else:
            if self._randomEnabled:
                if len(self._alreadyUsedTracks) >= 1: self._alreadyUsedTracks.pop()
                if len(self._alreadyUsedTracks) <= 0:
                    nextTrack = random.randint(0, (len(self._playlist) - 1))
                    while nextTrack == self._nowPlaying: nextTrack = random.randint(0, (len(self._playlist) - 1))
                else: nextTrack = self._alreadyUsedTracks[-1]
            else:
                if self._nowPlaying <= 0: nextTrack = (len(self._playlist) - 1)
                else: nextTrack = self._nowPlaying - 1
            self.changeMedia(nextTrack)
        if self._playbackState: self.play()

    def nextTrack(self) -> None:
        # if self.myParent.queuePlaylist.queue != []:
        #     nextTrack = self.myParent.queuePlaylist.queue[0]
        #     self.myParent.queuePlaylist.removeFromQueue(0)
        # else:
        if self._randomEnabled:
            if len(self._alreadyUsedTracks) == len(self._playlist): self._alreadyUsedTracks = []
            nextTrack = random.randint(0, (len(self._playlist) - 1))
            while nextTrack in self._alreadyUsedTracks: nextTrack = random.randint(0, (len(self._playlist) - 1))
            self._alreadyUsedTracks.append(nextTrack)
        else:
            if self._nowPlaying >= (len(self._playlist) - 1): nextTrack = 0
            else: nextTrack = self._nowPlaying + 1
        self.changeMedia(nextTrack)
        if self._playbackState: self.play()

    def mute(self) -> None:
        muteState = self._mediaPlayer.audioOutput().isMuted()
        if muteState: self._mediaPlayer.audioOutput().setMuted(False)
        else: self._mediaPlayer.audioOutput().setMuted(True)
        self._buttonInterface.changeMuteButton(not (muteState))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow("MP3 player")
    window.show()
    window.checkAudioOutThread.start()
    window.loadPlaylistThread.start()
    sys.exit(app.exec())

# pyinstaller -F -w -i "images/app.ico" -n "Media player" main.py