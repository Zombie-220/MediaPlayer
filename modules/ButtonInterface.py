from PyQt6.QtWidgets import QMainWindow, QSlider
from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtGui import QColor
from PyQt6.QtMultimedia import QMediaPlayer
import random, eyed3, time

from modules.SimpleModules import Label, Button, LineEntry
from modules.GlobalVariable import *

class MainWindow(QMainWindow):
    nowPlaying: int
    playbackState: bool
    repeatTrack: bool
    randomEnabled: bool
    listOfTracks: list[int]

    mediaPlayer: QMediaPlayer

class ButtonInterface(Label):
    def __init__(self, parent: MainWindow, x: int, y: int, width: int, height: int, objectName: str):
        super().__init__(parent, x, y, width, height, objectName, "")
        self.myParent = parent

        self.__btnPlay = Button(self, PLAY_ICON, 10, 10, 125, 50, "btn_orange", self.changePlaybackState)
        self.__btnPlay.setIconSize(QSize(30,30))
        self.__btnPlay.setShortcut(Qt.Key.Key_Space)
        self.__btnPlay.setToolTip("Проиграть")
        btnPrevious = Button(self, PREVIOUS_ICON, 10, self.__btnPlay.pos().y()+self.__btnPlay.height()+10, 60, 30, "btn_orange", self.previousTrack)
        btnPrevious.setShortcut(Qt.Key.Key_Left)
        btnPrevious.setToolTip("Предыдущий трэк")
        btnNext = Button(self, NEXT_ICON, btnPrevious.pos().x()+btnPrevious.width()+5, self.__btnPlay.pos().y()+self.__btnPlay.height()+10, 60, 30, "btn_orange", self.nextTrack)
        btnNext.setShortcut(Qt.Key.Key_Right)
        btnNext.setToolTip("Следующий трэк")

        btnReduceVolume = Button(self, REDUCE_VOLUME_ICON, self.__btnPlay.pos().x()+self.__btnPlay.width()+10, self.__btnPlay.pos().y(), 30, 30, "btn_orange", self.reduceVolume)
        btnReduceVolume.setToolTip("Уменьшить громкость")
        btnReduceVolume.setShortcut(Qt.Key.Key_Down)
        btnReduceVolume.setIconSize(QSize(20,20))
        self.__entryVolume = LineEntry(self, btnReduceVolume.pos().x()+btnReduceVolume.width()+5, btnReduceVolume.pos().y(), 70, 30, "", True, "entry")
        btnAddVolume = Button(self, ADD_VOLUME_ICON, self.__entryVolume.pos().x()+self.__entryVolume.width()+5, self.__entryVolume.pos().y(), 30, 30, "btn_orange", self.addVolume)
        btnAddVolume.setToolTip("Увеличить громкость")
        btnAddVolume.setShortcut(Qt.Key.Key_Up)
        btnAddVolume.setIconSize(QSize(20,20))
        self.__btnMute = Button(self, MUTE_ICON, btnAddVolume.pos().x(), btnAddVolume.pos().y()+btnAddVolume.height()+5, 30, 30, "btn_orange", self.mute)
        self.__btnMute.setToolTip("Выключить звук")
        self.__btnMute.setShortcut(Qt.Key.Key_M)
        self.__btnMute.setIconSize(QSize(20,20))
        self.__btnMute.setStyleSheet(SPECIAL_BTN_CSS)
        self.sliderVolume = QSlider(Qt.Orientation.Horizontal, self)
        self.sliderVolume.setRange(0, 100)
        self.sliderVolume.setFixedSize((btnAddVolume.pos().x()+btnAddVolume.width())-(self.__entryVolume.pos().x()), 15)
        self.sliderVolume.move(btnReduceVolume.pos().x(), btnReduceVolume.pos().y()+btnReduceVolume.height()+14)
        self.sliderVolume.valueChanged.connect(self.volumeChanged)
        self.sliderVolume.setValue(20)

        self.sliderDuration = QSlider(Qt.Orientation.Horizontal, self)
        self.sliderDuration.move(btnNext.pos().x() + btnNext.width() + 10, btnNext.pos().y() + 10)
        self.sliderDuration.setFixedSize(self.width() - (btnNext.pos().x() + btnNext.width() + 10) - 110, 15)
        self.sliderDuration.sliderPressed.connect(self.myParent.mediaPlayer.stop)
        self.sliderDuration.sliderReleased.connect(self.sliderReleased)
        self.sliderDuration.valueChanged.connect(self.changeTimecode)

        self.__entryDuration = LineEntry(self, self.sliderDuration.pos().x()+self.sliderDuration.width()+10, btnNext.pos().y(), 90, 30, "", True, "entry")
        self.__entryDuration.setText("0:00")

        self.__btnRandom = Button(self, RANDOM_ICON, btnAddVolume.pos().x()+btnAddVolume.width()+10, btnAddVolume.pos().y(), 30, 30, "btn_orange", self.enableRandom)
        self.__btnRandom.setIconSize(QSize(20,20))
        self.__btnRandom.setToolTip("Воспроизводить в случайном порядке")
        self.__btnRandom.setStyleSheet(SPECIAL_BTN_CSS)
        self.__btnRepeat = Button(self, REPEAT_ICON, self.__btnRandom.pos().x(), self.__btnMute.pos().y(), 30, 30, "btn_orange", self.enableRepeat)
        self.__btnRepeat.setIconSize(QSize(20,20))
        self.__btnRepeat.setToolTip("Включить повтор")
        self.__btnRepeat.setStyleSheet(SPECIAL_BTN_CSS)

        self.__labelNames = Label(self, self.__btnRandom.pos().x()+self.__btnRandom.width()+10, self.__btnRandom.pos().y(),
                                      (self.__entryDuration.pos().x()+self.__entryDuration.width())-(self.__btnRandom.pos().x()+self.__btnRandom.width()+10), 45,
                                      "label", "Исполнитель: >_<\nНазвание: >_<")
        self.__labelNames.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def changePlaybackState(self) -> None:
        match self.myParent.mediaPlayer.playbackState():
            case QMediaPlayer.PlaybackState.PlayingState:
                self.pause()
            case QMediaPlayer.PlaybackState.StoppedState:
                self.changeMedia(self.myParent.nowPlaying)
                self.play()
            case QMediaPlayer.PlaybackState.PausedState:
                self.play()

    def previousTrack(self) -> None:
        if self.myParent.mediaPlayer.position() > 5000: self.myParent.mediaPlayer.setPosition(0)
        else:
            if self.myParent.randomEnabled:
                if len(self.myParent.listOfTracks) >= 1: self.myParent.listOfTracks.pop()
                if len(self.myParent.listOfTracks) <= 0:
                    nextTrack = random.randint(1, len(self.myParent.playlist.playlist))
                    while nextTrack == self.myParent.nowPlaying: nextTrack = random.randint(1, len(self.myParent.playlist.playlist))
                else: nextTrack = self.myParent.listOfTracks[-1]
            else:
                if self.myParent.nowPlaying <= 1: nextTrack = len(self.myParent.playlist.playlist)
                else: nextTrack = self.myParent.nowPlaying - 1
            self.changeMedia(nextTrack)
        if self.myParent.playbackState: self.play()

    def nextTrack(self) -> None:
        if self.myParent.randomEnabled:
            if len(self.myParent.listOfTracks) == len(self.myParent.playlist.playlist): self.myParent.listOfTracks = []
            nextTrack = random.randint(1, len(self.myParent.playlist.playlist))
            while nextTrack in self.myParent.listOfTracks: nextTrack = random.randint(1, len(self.myParent.playlist.playlist))
            self.myParent.listOfTracks.append(nextTrack)
        else:
            if self.myParent.nowPlaying >= len(self.myParent.playlist.playlist): nextTrack = 1
            else: nextTrack = self.myParent.nowPlaying + 1
        self.changeMedia(nextTrack)
        if self.myParent.playbackState: self.play()

    def changeTimecode(self, d: int) -> None:
        m = d // 1000 // 60
        s = d // 1000 % 60
        self.__entryDuration.setText(f'{m:>1}:{s:0>2}')
        self.sliderDuration.setValue(d)

    def mediaStatusChanged(self, status: QMediaPlayer.MediaStatus) -> None:
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            if self.myParent.repeatTrack:
                self.myParent.mediaPlayer.setSource(QUrl())
                self.changeMedia(self.myParent.nowPlaying)
                self.play()
            else: self.nextTrack()

    def sliderReleased(self) -> None:
        self.myParent.mediaPlayer.stop()
        self.myParent.mediaPlayer.setPosition(self.sliderDuration.value())
        if self.myParent.playbackState: self.play()

    def changeMedia(self, musicID: int) -> None:
        newMedia = QUrl.fromLocalFile(Rf"{self.myParent.playlist.playlist[musicID]}")
        self.myParent.mediaPlayer.stop()
        time.sleep(0.5)
        self.myParent.mediaPlayer.setSource(newMedia)
        for i in range(self.myParent.playlist.columnCount()):
            try: self.myParent.playlist.item(self.myParent.nowPlaying-1, i).setBackground(QColor(0,0,0,0))
            except: pass
        self.myParent.nowPlaying = musicID
        for i in range(self.myParent.playlist.columnCount()):
            try: self.myParent.playlist.item(self.myParent.nowPlaying-1, i).setBackground(QColor(255,88,0,240))
            except: pass
        mp3 = eyed3.load(Rf"{self.myParent.playlist.playlist[musicID]}")
        if mp3.tag.artist == None: artist = ">_<"
        else: artist = mp3.tag.artist
        if mp3.tag.title == None: title = ">_<"
        else: title = mp3.tag.title
        self.__labelNames.setText(f"Исполнитель: {artist}\nНазвание: {title}")

    def play(self) -> None:
        self.myParent.mediaPlayer.play()
        self.myParent.playbackState = True
        self.__btnPlay.setIcon(PAUSE_ICON)
        self.__btnPlay.setToolTip("Остановить")
        self.myParent.miniWindow.btn_play.setIcon(PAUSE_ICON)
        self.myParent.miniWindow.setToolTip("Остановить")

    def pause(self) -> None:
        self.myParent.mediaPlayer.pause()
        self.myParent.playbackState = False
        self.__btnPlay.setIcon(PLAY_ICON)
        self.__btnPlay.setToolTip("Проиграть")
        self.myParent.miniWindow.btn_play.setIcon(PLAY_ICON)
        self.myParent.miniWindow.btn_play.setToolTip("Проиграть")

    def stop(self) -> None:
        self.myParent.mediaPlayer.stop()
        self.myParent.playbackState = False
        self.__btnPlay.setIcon(PLAY_ICON)
        self.__btnPlay.setToolTip("Проиграть")
        self.myParent.miniWindow.btn_play.setIcon(PLAY_ICON)
        self.myParent.miniWindow.btn_play.setToolTip("Проиграть")
        self.__labelNames.setText("Исполнитель: >_<\nНазвание: >_<")

    def reduceVolume(self) -> None:
        self.sliderVolume.setValue(self.sliderVolume.value()-1)

    def addVolume(self) -> None:
        self.sliderVolume.setValue(self.sliderVolume.value()+1)

    def volumeChanged(self, v: int) -> None:
        self.__entryVolume.setText(f"{v}")
        self.myParent.mediaPlayer.audioOutput().setVolume(v / 100)

    def mute(self) -> None:
        muteState = self.myParent.mediaPlayer.audioOutput().isMuted()
        if muteState:
            self.myParent.mediaPlayer.audioOutput().setMuted(False)
            self.__btnMute.setToolTip("Выключить звук")
            self.__btnMute.setObjectName("btn_orange")
        else:
            self.myParent.mediaPlayer.audioOutput().setMuted(True)
            self.__btnMute.setToolTip("Включить звук")
            self.__btnMute.setObjectName("btn_red")
        self.__btnMute.setStyleSheet(SPECIAL_BTN_CSS)

    def enableRepeat(self) -> None:
        self.myParent.repeatTrack = not (self.myParent.repeatTrack)
        if self.myParent.repeatTrack: self.__btnRepeat.setObjectName("btn_red")
        else: self.__btnRepeat.setObjectName("btn_orange")
        self.__btnRepeat.setStyleSheet(SPECIAL_BTN_CSS)

    def enableRandom(self) -> None:
        self.myParent.randomEnabled = not (self.myParent.randomEnabled)
        if self.myParent.randomEnabled: self.__btnRandom.setObjectName("btn_red")
        else: self.__btnRandom.setObjectName("btn_orange")
        self.__btnRandom.setStyleSheet(SPECIAL_BTN_CSS)