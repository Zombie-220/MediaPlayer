from PyQt6.QtWidgets import QMainWindow, QSlider, QTableWidget, QWidget
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtCore import QEvent

import threading

from modules.SimpleModules import Button, Label

class PlaylistTable(QTableWidget):
    playlist: dict
    path: str
    loadPlaylistThread: threading.Thread
    def menuPressed(self, action: QAction) -> None: ...
    def loadPlaylist(self, path: str) -> None: ...
    def eventFilter(self, source: QWidget, event: QEvent): ...
    def getPath(self) -> str: ...
    def changeDir(self) -> None: ...


class ButtonInterface(Label):
    sliderVolume: QSlider
    sliderDuration: QSlider
    def changePlaybackState(self) -> None: ...
    def previousTrack(self) -> None: ...
    def nextTrack(self) -> None: ...
    def changeTimecode(self, d: int) -> None: ...
    def mediaStatusChanged(self, status: QMediaPlayer.MediaStatus) -> None: ...
    def sliderReleased(self) -> None: ...
    def changeMedia(self, musicID: int) -> None: ...
    def play(self) -> None: ...
    def pause(self) -> None: ...
    def stop(self) -> None: ...
    def reduceVolume(self) -> None: ...
    def addVolume(self) -> None: ...
    def volumeChanged(self, v: int) -> None: ...
    def mute(self) -> None: ...
    def enableRepeat(self) -> None: ...
    def enableRandom(self) -> None: ...


class MiniWindow(QMainWindow):
    btn_play: Button


class WarningWindow(QMainWindow): ...


class QueuePlaylist(QTableWidget): ...


class MainWindow(QMainWindow):
    icon: QPixmap
    title: str
    nowPlaying: int
    playbackState: bool
    repeatTrack: bool
    randomEnabled: bool
    listOfTracks: list[int]
    mustCheckAudioOut: bool

    mediaPlayer: QMediaPlayer
    btn_openMiniWindow: Button
    playlist: PlaylistTable
    buttonInterface: ButtonInterface
    miniWindow: MiniWindow
    warningWindow: WarningWindow
    queuePlaylist: QueuePlaylist

    checkAudioOutThread: threading.Thread