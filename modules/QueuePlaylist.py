from PyQt6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, QWidget, QMenu
from PyQt6.QtCore import Qt, QEvent, QPoint
from PyQt6.QtGui import QAction
import eyed3

from MainWindowHeader import MainWindow

class QueuePlaylist(QTableWidget):
    def __init__(self, parent: MainWindow, x: int, y:int, width: int, height: int):
        self._parent = parent
        super().__init__(0,1,parent)

        self.setFixedSize(width, height)
        self.move(x, y)
        self.setObjectName('tablePlaylist')
        self.verticalHeader().setVisible(False)
        self.setColumnWidth(0,self.width())
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setHorizontalHeaderLabels(["Очередь"])
        self.viewport().installEventFilter(self)

        self._contextMenu = QMenu(self)
        self._contextMenu.setObjectName('contextMenu')
        self._contextMenu.addAction('Удалить из очереди')
        # self._contextMenu.triggered.connect(self.menuPressed)

        for i in range(101):
            self.insertRow(self.rowCount())
            self.setItem(self.rowCount()-1, 0, QTableWidgetItem(f"{i}-0"))