from PyQt6.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem, QWidget, QMenu, QHeaderView, QFileDialog
from PyQt6.QtCore import Qt, QEvent, QPoint
from PyQt6.QtGui import QAction, QColor
import os, eyed3, threading, time, sqlite3

from MainWindowHeader import MainWindow

class PlaylistTable(QTableWidget):
    def __init__(self, parent: MainWindow,
                 x: int, y:int, width: int, height: int):
        super().__init__(0, 3, parent)
        self._parent = parent

        self.setFixedSize(width, height)
        self.move(x, y)
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
        self._contextMenu.triggered.connect(self._menuPressed)

    def eventFilter(self, source: QWidget, event: QEvent):
        if (event.type() == QEvent.Type.MouseButtonPress and event.buttons() == Qt.MouseButton.RightButton):
            item = self.itemAt(event.pos())
            if item:
                self._contextMenu.move(self._parent.pos().x() + self.pos().x() + event.pos().x() + 15, self._parent.pos().y() + self.pos().y() + event.pos().y() + 40)
                self._contextMenu.show()
        elif (event.type() == QEvent.Type.MouseButtonDblClick and event.buttons() == Qt.MouseButton.LeftButton):
            item = self.itemAt(event.pos())
            if item:
                self._parent.changeMedia(self.itemAt(event.pos()).row())
                self._parent.play()
        return super(PlaylistTable, self).eventFilter(source, event)

    def _menuPressed(self, action: QAction) -> None:
        match action.text():
            case 'Воспроизвести':
                print("play")
            case 'Добавить в очередь':
                # self.myParent.queuePlaylist.addToQueue(self.itemAt(action.sender().pos() - self.myParent.pos() - self.pos() - QPoint(15,40)).row()+1)
                print("addToQueue")
            case 'Удалить':
                print("remove")

    def clearTable(self) -> None:
        while self.rowCount() > 0:
            self.removeRow(self.rowCount()-1)

    def addTableItem(self, pathToFile: str, file: str) -> None:
        self.insertRow(self.rowCount())
        mp3 = eyed3.load(f"{pathToFile}\\{file}")
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
        time.sleep(0.02)
        if self.verticalScrollBar().isVisible(): self.setColumnWidth(0, int((self.width() * 39.2) // 100))

    def changeMedia(self, oldTraackInt: int, newTrackInt: int) -> None:
        for i in range(self.columnCount()):
            try: self.item(oldTraackInt, i).setBackground(QColor(0,0,0,0))
            except: pass
            try: self.item(newTrackInt, i).setBackground(QColor(255,88,0,240))
            except: pass