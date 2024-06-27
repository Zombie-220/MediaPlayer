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
    def __init__(self, parent: MainWindow, x: int, y: int, width: int, height: int, objectName: str):
        super().__init__(parent, x, y, width, height, objectName, "")
        self._parent = parent

        # self._btnPlay = Button(self, PLAY_ICON, 10, 10, 125, 50, "btn_orange", self.changePlaybackState)
        self._btnPlay = Button(self, PLAY_ICON, 10, 10, 125, 50, "btn_orange")
        self._btnPlay.setIconSize(QSize(30,30))
        self._btnPlay.setShortcut(Qt.Key.Key_Space)
        self._btnPlay.setToolTip("Проиграть")
        # btnPrevious = Button(self, PREVIOUS_ICON, 10, self._btnPlay.pos().y()+self._btnPlay.height()+10, 60, 30, "btn_orange", self.previousTrack)
        btnPrevious = Button(self, PREVIOUS_ICON, 10, self._btnPlay.pos().y()+self._btnPlay.height()+10, 60, 30, "btn_orange")
        btnPrevious.setShortcut(Qt.Key.Key_Left)
        btnPrevious.setToolTip("Предыдущий трэк")
        # btnNext = Button(self, NEXT_ICON, btnPrevious.pos().x()+btnPrevious.width()+5, self._btnPlay.pos().y()+self._btnPlay.height()+10, 60, 30, "btn_orange", self.nextTrack)
        btnNext = Button(self, NEXT_ICON, btnPrevious.pos().x()+btnPrevious.width()+5, self._btnPlay.pos().y()+self._btnPlay.height()+10, 60, 30, "btn_orange")
        btnNext.setShortcut(Qt.Key.Key_Right)
        btnNext.setToolTip("Следующий трэк")

        # btnReduceVolume = Button(self, REDUCE_VOLUME_ICON, self._btnPlay.pos().x()+self._btnPlay.width()+10, self._btnPlay.pos().y(), 30, 30, "btn_orange", self.reduceVolume)
        btnReduceVolume = Button(self, REDUCE_VOLUME_ICON, self._btnPlay.pos().x()+self._btnPlay.width()+10, self._btnPlay.pos().y(), 30, 30, "btn_orange")
        btnReduceVolume.setToolTip("Уменьшить громкость")
        btnReduceVolume.setShortcut(Qt.Key.Key_Down)
        btnReduceVolume.setIconSize(QSize(20,20))
        self._entryVolume = LineEntry(self, btnReduceVolume.pos().x()+btnReduceVolume.width()+5, btnReduceVolume.pos().y(), 70, 30, "0", True, "dark-comp-radius")
        # btnAddVolume = Button(self, ADD_VOLUME_ICON, self._entryVolume.pos().x()+self._entryVolume.width()+5, self._entryVolume.pos().y(), 30, 30, "btn_orange", self.addVolume)
        btnAddVolume = Button(self, ADD_VOLUME_ICON, self._entryVolume.pos().x()+self._entryVolume.width()+5, self._entryVolume.pos().y(), 30, 30, "btn_orange")
        btnAddVolume.setToolTip("Увеличить громкость")
        btnAddVolume.setShortcut(Qt.Key.Key_Up)
        btnAddVolume.setIconSize(QSize(20,20))
        # self._btnMute = Button(self, MUTE_ICON, btnAddVolume.pos().x(), btnAddVolume.pos().y()+btnAddVolume.height()+5, 30, 30, "btn_orange", self.mute)
        self._btnMute = Button(self, MUTE_ICON, btnAddVolume.pos().x(), btnAddVolume.pos().y()+btnAddVolume.height()+5, 30, 30, "btn_orange")
        self._btnMute.setToolTip("Выключить звук")
        self._btnMute.setShortcut(Qt.Key.Key_M)
        self._btnMute.setIconSize(QSize(20,20))
        self._btnMute.setStyleSheet(CSS)
        self._sliderVolume = QSlider(Qt.Orientation.Horizontal, self)
        self._sliderVolume.setRange(0, 100)
        self._sliderVolume.setFixedSize((btnAddVolume.pos().x()+btnAddVolume.width())-(self._entryVolume.pos().x()), 15)
        self._sliderVolume.move(btnReduceVolume.pos().x(), btnReduceVolume.pos().y()+btnReduceVolume.height()+14)
        # self._sliderVolume.valueChanged.connect(self.volumeChanged)
        self._sliderVolume.setValue(20)

        self._sliderDuration = QSlider(Qt.Orientation.Horizontal, self)
        self._sliderDuration.move(btnNext.pos().x() + btnNext.width() + 10, btnNext.pos().y() + 10)
        self._sliderDuration.setFixedSize(self.width() - (btnNext.pos().x() + btnNext.width() + 10) - 110, 15)
        # self._sliderDuration.sliderPressed.connect(self._parent.mediaPlayer.stop)
        # self._sliderDuration.sliderReleased.connect(self.sliderReleased)
        # self._sliderDuration.valueChanged.connect(self.changeTimecode)

        self._entryDuration = LineEntry(self, self._sliderDuration.pos().x()+self._sliderDuration.width()+10, btnNext.pos().y(), 90, 30, "0:00", True, "dark-comp-radius")

        # self._btnRandom = Button(self, RANDOM_ICON, btnAddVolume.pos().x()+btnAddVolume.width()+10, btnAddVolume.pos().y(), 30, 30, "btn_orange", self.enableRandom)
        self._btnRandom = Button(self, RANDOM_ICON, btnAddVolume.pos().x()+btnAddVolume.width()+10, btnAddVolume.pos().y(), 30, 30, "btn_orange")
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