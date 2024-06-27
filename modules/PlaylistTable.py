from PyQt6.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem, QWidget, QMenu, QHeaderView, QFileDialog
from PyQt6.QtCore import Qt, QEvent, QPoint
from PyQt6.QtGui import QAction
import os, eyed3, threading, time, sqlite3

from MainWindowHeader import MainWindow

class PlaylistTable(QTableWidget):
    def __init__(self, parent: MainWindow,
                 x: int, y:int, width: int, height: int):
        super().__init__(0, 3, parent)
        self._parent = parent
        # self.playlist: dict = {}

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

        for i in range(101):
            self.insertRow(self.rowCount())
            self.setItem(self.rowCount()-1, 0, QTableWidgetItem(f"{i}-0"))
            self.setItem(self.rowCount()-1, 1, QTableWidgetItem(f"{i}-1"))
            self.setItem(self.rowCount()-1, 2, QTableWidgetItem(f"{i}-2"))

        self._contextMenu = QMenu(self)
        self._contextMenu.setObjectName('contextMenu')
        self._contextMenu.addAction('Воспроизвести')
        self._contextMenu.addAction('Добавить в очередь')
        self._contextMenu.addSeparator()
        self._contextMenu.addAction('Удалить')
        # self._contextMenu.triggered.connect(self.menuPressed)

        # self.loadPlaylistThread = threading.Thread(target=lambda:[self.loadPlaylist(self.path)])