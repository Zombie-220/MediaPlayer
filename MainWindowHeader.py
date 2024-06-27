from PyQt6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    nowPlaying: int

    def addToQueue(self, musicID: int) -> None: ...
    def nextTrack(self) -> None: ...
    def changePlaybackState(self): ...
    def previousTrack(self): ...