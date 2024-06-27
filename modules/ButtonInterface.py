from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtGui import QColor
from PyQt6.QtMultimedia import QMediaPlayer
import random, eyed3, time

from modules.SimpleModules import Label, Button, LineEntry
from modules.GlobalVariable import (PLAY_ICON, PREVIOUS_ICON, NEXT_ICON, REDUCE_VOLUME_ICON, ADD_VOLUME_ICON,
                                    MUTE_ICON, CSS, RANDOM_ICON, REPEAT_ICON, PAUSE_ICON)

from MainWindowHeader import MainWindow

class ButtonInterface(Label):
    def __init__(self, parent: MainWindow, x: int, y: int, width: int, height: int):
        super().__init__(parent, x, y, width, height, "", "")
        self._parent = parent

        # self._btnPlay = Button(self, PLAY_ICON, 10, 10, 125, 50, "btn_orange", self.changePlaybackState)
        self._btnPlay = Button(self, PLAY_ICON, 10, 10, 125, 50, "btn_orange")
        self._btnPlay.setIconSize(QSize(30,30))
        self._btnPlay.setShortcut(Qt.Key.Key_Space)
        self._btnPlay.setToolTip("Проиграть")
        # btn_previous = Button(self, PREVIOUS_ICON, 10, self._btnPlay.pos().y()+self._btnPlay.height()+10, 60, 30, "btn_orange", self.previousTrack)
        btn_previous = Button(self, PREVIOUS_ICON, 10, self._btnPlay.pos().y()+self._btnPlay.height()+10, 60, 30, "btn_orange")
        btn_previous.setShortcut(Qt.Key.Key_Left)
        btn_previous.setToolTip("Предыдущий трэк")
        # btn_next = Button(self, NEXT_ICON, btn_previous.pos().x()+btn_previous.width()+5, self._btnPlay.pos().y()+self._btnPlay.height()+10, 60, 30, "btn_orange", self.nextTrack)
        btn_next = Button(self, NEXT_ICON, btn_previous.pos().x()+btn_previous.width()+5, self._btnPlay.pos().y()+self._btnPlay.height()+10, 60, 30, "btn_orange")
        btn_next.setShortcut(Qt.Key.Key_Right)
        btn_next.setToolTip("Следующий трэк")

        # btn_reduceVolume = Button(self, REDUCE_VOLUME_ICON, self._btnPlay.pos().x()+self._btnPlay.width()+10, self._btnPlay.pos().y(), 30, 30, "btn_orange", self.reduceVolume)
        btn_reduceVolume = Button(self, REDUCE_VOLUME_ICON, self._btnPlay.pos().x()+self._btnPlay.width()+10, self._btnPlay.pos().y(), 30, 30, "btn_orange")
        btn_reduceVolume.setToolTip("Уменьшить громкость")
        btn_reduceVolume.setShortcut(Qt.Key.Key_Down)
        btn_reduceVolume.setIconSize(QSize(20,20))
        self._entryVolume = LineEntry(self, btn_reduceVolume.pos().x()+btn_reduceVolume.width()+5, btn_reduceVolume.pos().y(), 70, 30, "0", True, "dark-comp-radius")
        # btn_addVolume = Button(self, ADD_VOLUME_ICON, self._entryVolume.pos().x()+self._entryVolume.width()+5, self._entryVolume.pos().y(), 30, 30, "btn_orange", self.addVolume)
        btn_addVolume = Button(self, ADD_VOLUME_ICON, self._entryVolume.pos().x()+self._entryVolume.width()+5, self._entryVolume.pos().y(), 30, 30, "btn_orange")
        btn_addVolume.setToolTip("Увеличить громкость")
        btn_addVolume.setShortcut(Qt.Key.Key_Up)
        btn_addVolume.setIconSize(QSize(20,20))
        # self._btnMute = Button(self, MUTE_ICON, btn_addVolume.pos().x(), btn_addVolume.pos().y()+btn_addVolume.height()+5, 30, 30, "btn_orange", self.mute)
        self._btnMute = Button(self, MUTE_ICON, btn_addVolume.pos().x(), btn_addVolume.pos().y()+btn_addVolume.height()+5, 30, 30, "btn_orange")
        self._btnMute.setToolTip("Выключить звук")
        self._btnMute.setShortcut(Qt.Key.Key_M)
        self._btnMute.setIconSize(QSize(20,20))
        self._btnMute.setStyleSheet(CSS)
        self._sliderVolume = QSlider(Qt.Orientation.Horizontal, self)
        self._sliderVolume.setRange(0, 100)
        self._sliderVolume.setFixedSize((btn_addVolume.pos().x()+btn_addVolume.width())-(self._entryVolume.pos().x()), 15)
        self._sliderVolume.move(btn_reduceVolume.pos().x(), btn_reduceVolume.pos().y()+btn_reduceVolume.height()+14)
        # self._sliderVolume.valueChanged.connect(self.volumeChanged)
        self._sliderVolume.setValue(20)

        self._sliderDuration = QSlider(Qt.Orientation.Horizontal, self)
        self._sliderDuration.move(btn_next.pos().x() + btn_next.width() + 10, btn_next.pos().y() + 10)
        self._sliderDuration.setFixedSize(self.width() - (btn_next.pos().x() + btn_next.width() + 10) - 110, 15)
        # self._sliderDuration.sliderPressed.connect(self._parent.mediaPlayer.stop)
        # self._sliderDuration.sliderReleased.connect(self.sliderReleased)
        # self._sliderDuration.valueChanged.connect(self.changeTimecode)

        self._entryDuration = LineEntry(self, self._sliderDuration.pos().x()+self._sliderDuration.width()+10, btn_next.pos().y(), 90, 30, "0:00", True, "dark-comp-radius")

        # self._btnRandom = Button(self, RANDOM_ICON, btn_addVolume.pos().x()+btn_addVolume.width()+10, btn_addVolume.pos().y(), 30, 30, "btn_orange", self.enableRandom)
        self._btnRandom = Button(self, RANDOM_ICON, btn_addVolume.pos().x()+btn_addVolume.width()+10, btn_addVolume.pos().y(), 30, 30, "btn_orange")
        self._btnRandom.setIconSize(QSize(20,20))
        self._btnRandom.setToolTip("Воспроизводить в случайном порядке")
        self._btnRandom.setStyleSheet(CSS)
        # self._btnRepeat = Button(self, REPEAT_ICON, self._btnRandom.pos().x(), self._btnMute.pos().y(), 30, 30, "btn_orange", self.enableRepeat)
        self._btnRepeat = Button(self, REPEAT_ICON, self._btnRandom.pos().x(), self._btnMute.pos().y(), 30, 30, "btn_orange")
        self._btnRepeat.setIconSize(QSize(20,20))
        self._btnRepeat.setToolTip("Включить повтор")
        self._btnRepeat.setStyleSheet(CSS)

        self._btnRepeat = Label(self, self._btnRandom.pos().x()+self._btnRandom.width()+10, self._btnRandom.pos().y(),
                                      (self._entryDuration.pos().x()+self._entryDuration.width())-(self._btnRandom.pos().x()+self._btnRandom.width()+10), 45,
                                      "label", "Исполнитель: >_<\nНазвание: >_<")
        self._btnRepeat.setAlignment(Qt.AlignmentFlag.AlignLeft)