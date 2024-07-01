from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt, QSize
import eyed3

from modules.SimpleModules import Label, Button, LineEntry
from modules.GlobalVariable import PLAY_ICON, PREVIOUS_ICON, NEXT_ICON, REDUCE_VOLUME_ICON, ADD_VOLUME_ICON, MUTE_ICON, RANDOM_ICON, REPEAT_ICON, PAUSE_ICON
from modules.GlobalVariable import CSS

from MainWindowHeader import MainWindow

class ButtonInterface(Label):
    def __init__(self, parent: MainWindow, x: int, y: int, width: int, height: int):
        super().__init__(parent, x, y, width, height, "", "")
        self.__parent = parent

        self.__btnPlay = Button(self, PLAY_ICON, 10, 10, 125, 50, "btn_orange", self.__parent.changePlaybackState)
        self.__btnPlay.setIconSize(QSize(30,30))
        self.__btnPlay.setShortcut(Qt.Key.Key_Space)
        self.__btnPlay.setToolTip("Проиграть")
        btn_previous = Button(self, PREVIOUS_ICON, 10, self.__btnPlay.pos().y()+self.__btnPlay.height()+10, 60, 30, "btn_orange", self.__parent.previousTrack)
        btn_previous.setShortcut(Qt.Key.Key_Left)
        btn_previous.setToolTip("Предыдущий трэк")
        btn_next = Button(self, NEXT_ICON, btn_previous.pos().x()+btn_previous.width()+5, self.__btnPlay.pos().y()+self.__btnPlay.height()+10, 60, 30, "btn_orange", self.__parent.nextTrack)
        btn_next.setShortcut(Qt.Key.Key_Right)
        btn_next.setToolTip("Следующий трэк")

        btn_reduceVolume = Button(self, REDUCE_VOLUME_ICON, self.__btnPlay.pos().x()+self.__btnPlay.width()+10, self.__btnPlay.pos().y(), 30, 30, "btn_orange", lambda: [self.__sliderVolume.setValue(self.__sliderVolume.value()-1)])
        btn_reduceVolume.setToolTip("Уменьшить громкость")
        btn_reduceVolume.setShortcut(Qt.Key.Key_Down)
        btn_reduceVolume.setIconSize(QSize(20,20))
        self.__entryVolume = LineEntry(self, btn_reduceVolume.pos().x()+btn_reduceVolume.width()+5, btn_reduceVolume.pos().y(), 70, 30, "0", True, "dark-comp-radius")
        btn_addVolume = Button(self, ADD_VOLUME_ICON, self.__entryVolume.pos().x()+self.__entryVolume.width()+5, self.__entryVolume.pos().y(), 30, 30, "btn_orange", lambda: [self.__sliderVolume.setValue(self.__sliderVolume.value()+1)])
        btn_addVolume.setToolTip("Увеличить громкость")
        btn_addVolume.setShortcut(Qt.Key.Key_Up)
        btn_addVolume.setIconSize(QSize(20,20))
        self.__btnMute = Button(self, MUTE_ICON, btn_addVolume.pos().x(), btn_addVolume.pos().y()+btn_addVolume.height()+5, 30, 30, "btn_orange", self.__parent.mute)
        self.__btnMute.setToolTip("Выключить звук")
        self.__btnMute.setShortcut(Qt.Key.Key_M)
        self.__btnMute.setIconSize(QSize(20,20))
        self.__btnMute.setStyleSheet(CSS)
        self.__sliderVolume = QSlider(Qt.Orientation.Horizontal, self)
        self.__sliderVolume.setRange(0, 100)
        self.__sliderVolume.setFixedSize((btn_addVolume.pos().x()+btn_addVolume.width())-(self.__entryVolume.pos().x()), 15)
        self.__sliderVolume.move(btn_reduceVolume.pos().x(), btn_reduceVolume.pos().y()+btn_reduceVolume.height()+14)
        self.__sliderVolume.valueChanged.connect(self.__volumeChanged)
        self.__sliderVolume.setValue(20)

        self.__sliderDuration = QSlider(Qt.Orientation.Horizontal, self)
        self.__sliderDuration.move(btn_next.pos().x() + btn_next.width() + 10, btn_next.pos().y() + 10)
        self.__sliderDuration.setFixedSize(self.width() - (btn_next.pos().x() + btn_next.width() + 10) - 110, 15)
        self.__sliderDuration.sliderPressed.connect(self.__parent.stopMedia)
        self.__sliderDuration.sliderReleased.connect(lambda: [self.__parent.setMediaPosition(self.__sliderDuration.value())])
        self.__sliderDuration.valueChanged.connect(lambda d: [self.__entryDuration.setText(f"{(d//1000//60):>1}:{(d//1000%60):0>2}")])

        self.__entryDuration = LineEntry(self, self.__sliderDuration.pos().x()+self.__sliderDuration.width()+10, btn_next.pos().y(), 90, 30, "0:00", True, "dark-comp-radius")

        self.__btnRandom = Button(self, RANDOM_ICON, btn_addVolume.pos().x()+btn_addVolume.width()+10, btn_addVolume.pos().y(), 30, 30, "btn_orange", self.__parent.changeRandom)
        self.__btnRandom.setIconSize(QSize(20,20))
        self.__btnRandom.setToolTip("Воспроизводить в случайном порядке")
        self.__btnRandom.setStyleSheet(CSS)
        self.__btnRepeat = Button(self, REPEAT_ICON, self.__btnRandom.pos().x(), self.__btnMute.pos().y(), 30, 30, "btn_orange", self.__parent.changeRepeat)
        self.__btnRepeat.setIconSize(QSize(20,20))
        self.__btnRepeat.setToolTip("Включить повтор")
        self.__btnRepeat.setStyleSheet(CSS)

        self.__labelNames = Label(self, self.__btnRandom.pos().x()+self.__btnRandom.width()+10, self.__btnRandom.pos().y(),
                                      (self.__entryDuration.pos().x()+self.__entryDuration.width())-(self.__btnRandom.pos().x()+self.__btnRandom.width()+10), 45,
                                      "label", "Исполнитель: >-<\nНазвание: >-<")
        self.__labelNames.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def changeMedia(self, linkToMP3: str) -> None:
        mp3 = eyed3.load(linkToMP3)
        title = ">-<"
        artist =  ">-<"
        if mp3.tag:
            if mp3.tag.artist: artist = mp3.tag.artist
            if mp3.tag.title: title = mp3.tag.title
        else:
            title = linkToMP3[linkToMP3.rfind("\\")+1:linkToMP3.rfind(".")]
        self.__labelNames.setText(f"Исполнитель: {artist}\nНазвание: {title}")

    def changePlayButton(self, playbackState: bool) -> None:
        if playbackState: self.__btnPlay.setIcon(PAUSE_ICON)
        else: self.__btnPlay.setIcon(PLAY_ICON)

    def changeRandomButton(self, randomEnabled: bool) -> None:
        if randomEnabled: self.__btnRandom.setObjectName("btn_red")
        else: self.__btnRandom.setObjectName("btn_orange")
        self.setStyleSheet(CSS)

    def changeMuteButton(self, muteEnabled: bool) -> None:
        if muteEnabled:
            self.__btnMute.setObjectName("btn_red")
            self.__btnMute.setToolTip("Включить звук")
        else:
            self.__btnMute.setObjectName("btn_orange")
            self.__btnMute.setToolTip("Выключить звук")
        self.setStyleSheet(CSS)

    def changeRepeatButton(self, enableRepeat: bool) -> None:
        if enableRepeat: self.__btnRepeat.setObjectName("btn_red")
        else: self.__btnRepeat.setObjectName("btn_orange")
        self.setStyleSheet(CSS)

    def __volumeChanged(self, volume: int) -> None:
        self.__entryVolume.setText(f"{volume}")
        self.__parent.changeVolume(volume / 100)

    def changeDuration(self, d: int) -> None: self.__sliderDuration.setRange(0, d)
    def setDuration(self, d: int) -> None: self.__sliderDuration.setValue(d)

    def getValue(self) -> int:
        return self.__sliderVolume.value()