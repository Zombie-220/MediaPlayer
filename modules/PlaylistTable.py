from PyQt6.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem, QWidget, QMenu, QHeaderView, QFileDialog
from PyQt6.QtCore import Qt, QEvent, QPoint
from PyQt6.QtGui import QAction
import os, eyed3, threading, time, sqlite3

from MainWindowHeader import MainWindow

class PlaylistTable(QTableWidget):
    def __init__(self, parent: MainWindow,
                 xPos: int, yPos:int, width: int, height: int):
        super().__init__(0, 3, parent)
        self._parent = parent
        self.playlist: dict = {}

        self.setObjectName("tablePlaylist")
        self.setFixedSize(width, height)
        self.move(xPos, yPos)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setColumnWidth(0, ((self.width() * 40) // 100))
        self.setColumnWidth(1, ((self.width() * 40) // 100))
        self.setColumnWidth(2, ((self.width() * 20) // 100))
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignBottom)
        self.setHorizontalHeaderLabels(["Название", "Исполнтель", "Длительность"])
        self.viewport().installEventFilter(self)

        self._contextMenu = QMenu(self)
        self._contextMenu.setObjectName('contextMenu')
        self._contextMenu.addAction('Воспроизвести')
        self._contextMenu.addAction('Добавить в очередь')
        self._contextMenu.addSeparator()
        self._contextMenu.addAction('Удалить')
        self._contextMenu.triggered.connect(self.menuPressed)

        self.path = self.getPath()
        self.loadPlaylistThread = threading.Thread(target=lambda:[self.loadPlaylist(self.path)])

    def menuPressed(self, action: QAction) -> None:
        match action.text():
            case 'Воспроизвести':
                print("play")
            case 'Добавить в очередь':
                self._parent.addToQueue(self.itemAt(action.sender().pos() - self._parent.pos() - self.pos() - QPoint(15,40)).row()+1)
            case 'Удалить':
                print("remove")

    def loadPlaylist(self, path: str) -> None:
        while self.rowCount() > 0:
            self.removeRow(self.rowCount()-1)
        self._parent.nowPlaying = 1
        count = 0
        dictOfMedia = {}
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.mp3'):
                    mp3 = eyed3.load(f"{path}\{file}")
                    self.insertRow(self.rowCount())
                    if mp3.tag != None:
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
                    dictOfMedia[count] = f"{path}\\{file}"
            break
        self.playlist = dictOfMedia
        if self.playlist == {}:
            self._parent.buttonInterface.setDisabled(True)
            self._parent.btn_openMiniWindow.setDisabled(True)
        else:
            self._parent.buttonInterface.setDisabled(False)
            self._parent.btn_openMiniWindow.setDisabled(False)
        time.sleep(0.05)
        if self.verticalScrollBar().isVisible():
            self.setColumnWidth(0, ((self.width() * 40) // 100))

    def eventFilter(self, source: QWidget, event: QEvent):
        if (event.type() == QEvent.Type.MouseButtonPress and event.buttons() == Qt.MouseButton.RightButton):
            item = self.itemAt(event.pos())
            if item:
                self._contextMenu.move(self._parent.pos().x() + self.pos().x() + event.pos().x() + 15, self._parent.pos().y() + self.pos().y() + event.pos().y() + 40)
                self._contextMenu.show()
                pass
        elif (event.type() == QEvent.Type.MouseButtonDblClick and event.buttons() == Qt.MouseButton.LeftButton):
            item = self.itemAt(event.pos())
            if item:
                self._parent.buttonInterface.changeMedia(self.itemAt(event.pos()).row()+1)
                self._parent.buttonInterface.play()
        return super(PlaylistTable, self).eventFilter(source, event)

    def getPath(self) -> str:
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

    def changeDir(self) -> None:
        self._parent.buttonInterface.stop()
        newPath = QFileDialog.getExistingDirectory(directory=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        dirHasMP3 = False

        for root, dirs, files in os.walk(newPath):
            for file in files:
                if file.endswith(".mp3"):
                    dirHasMP3 = True
                    break
            break

        if not (dirHasMP3):
            self._parent.warningWindow.show()
            self._parent.setDisabled(True)
        else:
            self.path = newPath
            loadListThread = threading.Thread(target=lambda:[self.loadPlaylist(self.path)])
            loadListThread.start()

            connect = sqlite3.connect("database.db")
            cursor = connect.cursor()
            
            cursor.execute("UPDATE pathToDir SET path=?", (self.path,))

            connect.commit()
            connect.close()