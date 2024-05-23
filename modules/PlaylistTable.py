from PyQt6.QtWidgets import QMainWindow, QTableWidget, QAbstractItemView, QTableWidgetItem, QWidget, QMenu, QHeaderView
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QAction
import os, eyed3
import threading
import time

class MainWindow(QMainWindow):
    def changeMedia(self, musicID: int) -> None: ...

class PlaylistTable(QTableWidget):
    def __init__(self, parent: MainWindow,
                 xPos: int, yPos:int, width: int, height: int):
        super().__init__(0, 3, parent)
        self.myParent = parent
        self.playlist: dict = {}

        self.setObjectName("tablePlaylist")
        self.setFixedSize(width, height)
        self.move(xPos, yPos)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setColumnWidth(0, ((parent.width() * 40) // 100))
        self.setColumnWidth(1, ((parent.width() * 40) // 100))
        self.setColumnWidth(2, ((parent.width() * 20) // 100))
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignBottom)
        self.setHorizontalHeaderLabels(["Название", "Исполнтель", "Длительность"])
        self.viewport().installEventFilter(self)

        self.__contextMenu = QMenu()
        self.__contextMenu.addAction('Воспроизвести')
        self.__contextMenu.addAction('Удалить')
        self.__contextMenu.triggered.connect(self.menuPressed)

        path = R'C:\Users\Zombie\Desktop\по мелочи\music'
        self.loadPlaylistThread = threading.Thread(target=lambda:[self.loadPlaylist(path)])

    def menuPressed(self, action: QAction) -> None:
        match action.text():
            case 'Воспроизвести':
                print("play")
            case 'Удалить':
                print("remove")

    def loadPlaylist(self, path: str) -> None:
        count = 0
        dist = {}
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.mp3'):
                    mp3 = eyed3.load(f"{path}\{file}")

                    self.insertRow(self.rowCount())
                    if mp3.tag.title != None and mp3.tag.artist != None:
                        self.setItem(self.rowCount()-1, 0, QTableWidgetItem(mp3.tag.title))
                        self.setItem(self.rowCount()-1, 1, QTableWidgetItem(mp3.tag.artist))
                        duration = f"{int(mp3.info.time_secs//60):02}:{int(mp3.info.time_secs%60):02}"
                    else:
                        time.sleep(0.05)
                        self.setSpan(self.rowCount()-1, 0, 1, 2)
                        self.setItem(self.rowCount()-1, 0, QTableWidgetItem(f'{file}'))
                        duration = "--:--"
                    self.setItem(self.rowCount()-1, 2, QTableWidgetItem(duration))
                    count += 1
                    dist[count] = f"{path}\\{file}"
        self.playlist = dist
        time.sleep(0.05)
        if self.verticalScrollBar().isVisible():
            self.setColumnWidth(0, ((self.myParent.width() * 39) // 100))

    def eventFilter(self, source: QWidget, event: QEvent):
        if (event.type() == QEvent.Type.MouseButtonPress and event.buttons() == Qt.MouseButton.RightButton):
            item = self.itemAt(event.pos())
            if item:
                self.__contextMenu.move(event.pos().x() + self.myParent.pos().x(), event.pos().y() + self.myParent.pos().y())
                self.__contextMenu.show()
        elif (event.type() == QEvent.Type.MouseButtonDblClick and event.buttons() == Qt.MouseButton.LeftButton):
            item = self.itemAt(event.pos())
            if item:
                self.myParent.changeMedia(self.itemAt(event.pos()).row()+1)
        return super(PlaylistTable, self).eventFilter(source, event)