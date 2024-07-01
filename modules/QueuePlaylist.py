from PyQt6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, QWidget, QMenu
from PyQt6.QtCore import Qt, QEvent, QPoint
from PyQt6.QtGui import QAction
import eyed3

from MainWindowHeader import MainWindow

class QueuePlaylist(QTableWidget):
    def __init__(self, parent: MainWindow, x: int, y:int, width: int, height: int):
        self.__parent = parent
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

        self.__contextMenu = QMenu(self)
        self.__contextMenu.setObjectName('contextMenu')
        self.__contextMenu.addAction('Удалить из очереди')
        self.__contextMenu.triggered.connect(self.__menuPressed)

        for i in range(101):
            self.insertRow(self.rowCount())
            self.setItem(self.rowCount()-1, 0, QTableWidgetItem(f"{i}-0"))

    def eventFilter(self, source: QWidget, event: QEvent):
        if (event.type() == QEvent.Type.MouseButtonPress and event.buttons() == Qt.MouseButton.RightButton):
            item = self.itemAt(event.pos())
            if item:
                self.__contextMenu.move(self.__parent.pos().x()+self.pos().x()+event.pos().x()+15, self.__parent.pos().y()+self.pos().y()+event.pos().y()+48)
                self.__contextMenu.show()
        return super(QueuePlaylist, self).eventFilter(source, event)

    def __menuPressed(self, action: QAction) -> None:
        match action.text():
            case "Удалить из очереди":
                print("removeFromQueue")

    # def addToQueue(self, musicID: int) -> None:
    #     tempTrack = self.myParent.playlist.playlist[musicID]
    #     mp3 = eyed3.load(tempTrack)
    #     if mp3.tag:
    #         if mp3.tag.title: title = mp3.tag.title
    #     else:
    #         fullTitle = Rf"{self.myParent.playlist.playlist[musicID]}"
    #         title = fullTitle[fullTitle.rfind("\\")+1:-4]
    #     self.insertRow(self.rowCount())
    #     self.setItem(self.rowCount()-1, 0, QTableWidgetItem(title))
    #     self.queue.append(musicID)

    # def removeFromQueue(self, musicID: int) -> None:
    #     self.queue.pop(musicID)
    #     self.removeRow(musicID)