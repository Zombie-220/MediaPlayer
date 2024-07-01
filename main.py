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
        self.__icon: QPixmap = APP_ICON
        self.__title: str = title
        self.__mustCheckAudioOut: bool = True
        self.__nowPlaying: int = 0
        self.__playlist: list[str] = []
        self.__playbackState: bool = False
        self.__randomEnabled: bool = False
        self.__alreadyUsedTracks: list[int] = []
        self.__repeatEnabled: bool = False

        # self.queue: list[int] = []

        # self.repeatTrack: bool = False
        # self.randomEnabled: bool = False

        self.setWindowIcon(QIcon(self.__icon))
        self.setWindowTitle(self.__title)
        self.setStyleSheet(CSS)
        self.setObjectName("MainWindow")
        self.setFixedSize(960, 560)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.__mediaPlayer = QMediaPlayer(self)
        self.__audioOutput = QAudioOutput(self)
        self.__audioOutput.setVolume(0.2)
        self.__mediaPlayer.setAudioOutput(self.__audioOutput)
        self.__mediaPlayer.durationChanged.connect(lambda d: [self.__buttonInterface.changeDuration(d)])
        self.__mediaPlayer.positionChanged.connect(lambda d: [self.__buttonInterface.setDuration(d)])
        self.__mediaPlayer.mediaStatusChanged.connect(self.__mediaStatusChanged)

        windowHat = WindowTitleBar(self, self.__icon, self.__title, "dark-comp")
        self.__buttonInterface = ButtonInterface(self, 1, self.height()-111, self.width()-2, 110)
        self.__playlistTable = PlaylistTable(self, 1, windowHat.height(), ((self.width()-2) * 80) // 100, self.height()-(windowHat.height()+self.__buttonInterface.height()))
        self.__queueTable = QueuePlaylist(self, self.__playlistTable.width()+1, windowHat.height(), ((self.width()-2) * 20) // 100, self.height()-(windowHat.height()+self.__buttonInterface.height()))

        btn_close = Button(self, CLOSE_ICON, self.width()-30, 0, 30, 30, "btn_red_transp", self.closeEvent)
        btn_close.setToolTip("Закрыть окно")
        btn_showMinimize = Button(self, MINIMIZE_ICON, self.width()-60, 0, 30, 30, "btn_orange_transp", self.showMinimized)
        btn_showMinimize.setToolTip("Свернуть окно")
        btn_changeRep = Button(self, FOLDER_ICON, self.width()-120, 0, 30, 30, "btn_orange_transp", self.__changeDir)
        btn_changeRep.setToolTip("Выбрать папку")
        btn_changeRep.setIconSize(QSize(20,20))
        # self.__btn_openMiniWindow = Button(self, MINI_WINDOW_ICON, self.width()-90, 0, 30, 30, "btn_orange_transp", self.openMiniWindow)
        self.__btn_openMiniWindow = Button(self, MINI_WINDOW_ICON, self.width()-90, 0, 30, 30, "btn_orange_transp")
        self.__btn_openMiniWindow.setToolTip("Открыть мини проигрыватель")
        self.__btn_openMiniWindow.setIconSize(QSize(20,20))

        self.checkAudioOutThread = threading.Thread(target=self.__checkAudioOut)
        self.__path = self.__getPath()
        self.loadPlaylistThread = threading.Thread(target=lambda: [self.__loadPlaylist(self.__path)])

    def closeEvent(self, event) -> None:
        self.__mustCheckAudioOut = False
        self.close()

    def __checkAudioOut(self) -> None:
        while self.__mustCheckAudioOut:
            if self.__mediaPlayer.audioOutput() != None:
                if self.__mediaPlayer.audioOutput().device() != QAudioOutput().device():
                    self.__audioOutput = QAudioOutput()
                    self.__audioOutput.setVolume(self.__buttonInterface.getValue() / 100)
                    self.__mediaPlayer.setAudioOutput(self.__audioOutput)
            else:
                self.__audioOutput = QAudioOutput()
                self.__audioOutput.setVolume(self.__buttonInterface.getValue() / 100)
                self.__mediaPlayer.setAudioOutput(self.__audioOutput)
            time.sleep(1)

    def __loadPlaylist(self, path: str) -> None:
        self.__playlist = []
        self.__playlistTable.clearTable()
        self.__nowPlaying = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.mp3'):
                    self.__playlist.append(f"{path}\\{file}")
                    self.__playlistTable.addTableItem(path, file)
            break
        if self.__playlist == []: self.__buttonInterface.setDisabled(True)
        else: self.__buttonInterface.setDisabled(False)

    def __changeDir(self) -> None:
        self.stop()
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
            self.__path = newPath
            self.loadPlaylistThread = threading.Thread(target=lambda: [self.__loadPlaylist(self.__path)])
            self.loadPlaylistThread.start()

            connect = sqlite3.connect("database.db")
            cursor = connect.cursor()
            cursor.execute("UPDATE pathToDir SET path=?", (self.__path,))
            connect.commit()
            connect.close()

    def __getPath(self) -> str:
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
        newMedia = QUrl.fromLocalFile(Rf"{self.__playlist[musicID]}")
        self.__mediaPlayer.stop()
        time.sleep(0.5)
        self.__mediaPlayer.setSource(newMedia)

        self.__playlistTable.changeMedia(self.__nowPlaying, musicID)
        self.__buttonInterface.changeMedia(self.__playlist[musicID])

        self.__nowPlaying = musicID

    def play(self) -> None:
        self.__mediaPlayer.play()
        self.__playbackState = True
        self.__buttonInterface.changePlayButton(self.__playbackState)

    def stop(self) -> None:
        self.__mediaPlayer.stop()
        self.__playbackState = False
        self.__buttonInterface.changePlayButton(self.__playbackState)

    def pause(self) -> None:
        self.__mediaPlayer.pause()
        self.__playbackState = False
        self.__buttonInterface.changePlayButton(self.__playbackState)

    def changePlaybackState(self) -> None:
        match self.__mediaPlayer.playbackState():
            case QMediaPlayer.PlaybackState.StoppedState:
                if self.__randomEnabled:
                    if len(self.__playlist) == len(self.__alreadyUsedTracks): self.__alreadyUsedTracks = []
                    nextTrack = random.randint(0, len(self.__playlist))
                    while nextTrack in self.__alreadyUsedTracks: nextTrack = random.randint(0, len(self.__playlist))
                else: nextTrack = self.__nowPlaying
                self.changeMedia(nextTrack)
                self.play()
            case QMediaPlayer.PlaybackState.PlayingState: self.pause()
            case QMediaPlayer.PlaybackState.PausedState: self.play()

    def changeRandom(self) -> None:
        self.__randomEnabled = not self.__randomEnabled
        self.__buttonInterface.changeRandomButton(self.__randomEnabled)

    def changeRepeat(self) -> None:
        self.__repeatEnabled = not self.__repeatEnabled
        self.__buttonInterface.changeRepeatButton(self.__repeatEnabled)

    def previousTrack(self) -> None:
        if self.__mediaPlayer.position() > 5000: self.__mediaPlayer.setPosition(0)
        else:
            if self.__randomEnabled:
                if len(self.__alreadyUsedTracks) >= 1: self.__alreadyUsedTracks.pop()
                if len(self.__alreadyUsedTracks) <= 0:
                    nextTrack = random.randint(0, (len(self.__playlist) - 1))
                    while nextTrack == self.__nowPlaying: nextTrack = random.randint(0, (len(self.__playlist) - 1))
                else: nextTrack = self.__alreadyUsedTracks[-1]
            else:
                if self.__nowPlaying <= 0: nextTrack = (len(self.__playlist) - 1)
                else: nextTrack = self.__nowPlaying - 1
            self.changeMedia(nextTrack)
        if self.__playbackState: self.play()

    def nextTrack(self) -> None:
        # if self.myParent.queuePlaylist.queue != []:
        #     nextTrack = self.myParent.queuePlaylist.queue[0]
        #     self.myParent.queuePlaylist.removeFromQueue(0)
        # else:
        if self.__randomEnabled:
            if len(self.__alreadyUsedTracks) == len(self.__playlist): self.__alreadyUsedTracks = []
            nextTrack = random.randint(0, (len(self.__playlist) - 1))
            while nextTrack in self.__alreadyUsedTracks: nextTrack = random.randint(0, (len(self.__playlist) - 1))
            self.__alreadyUsedTracks.append(nextTrack)
        else:
            if self.__nowPlaying >= (len(self.__playlist) - 1): nextTrack = 0
            else: nextTrack = self.__nowPlaying + 1
        self.changeMedia(nextTrack)
        if self.__playbackState: self.play()

    def mute(self) -> None:
        muteState = self.__mediaPlayer.audioOutput().isMuted()
        if muteState: self.__mediaPlayer.audioOutput().setMuted(False)
        else: self.__mediaPlayer.audioOutput().setMuted(True)
        self.__buttonInterface.changeMuteButton(not (muteState))

    def changeVolume(self, volume: float) -> None: self.__mediaPlayer.audioOutput().setVolume(volume)
    def stopMedia(self) -> None: self.__mediaPlayer.stop()

    def setMediaPosition(self, value: int) -> None:
        self.__mediaPlayer.setPosition(value)
        if self.__playbackState: self.play()

    def __mediaStatusChanged(self, status: QMediaPlayer.MediaStatus) -> None:
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            if self.__repeatEnabled:
                self.__mediaPlayer.setSource(QUrl())
                self.changeMedia(self.__nowPlaying)
                self.play()
            else: self.nextTrack()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow("MP3 player")
    window.show()
    window.checkAudioOutThread.start()
    window.loadPlaylistThread.start()
    sys.exit(app.exec())

# pyinstaller -F -w -i "images/app.ico" -n "Media player" main.py