from PyQt6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, QWidget, QMenu
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QAction

from MainWindowHeader import MainWindow

class QueuePlaylist(QTableWidget):
    def __init__(self, parent: MainWindow, xPos: int, yPos:int, width: int, height: int):
        self.myParent = parent
        super().__init__(0,1,parent)

        self.setFixedSize(width, height)
        self.move(xPos, yPos)
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
        self.__contextMenu.triggered.connect(self.menuPressed)

        for i in range(101):
            self.insertRow(self.rowCount())
            self.setItem(self.rowCount()-1, 0, QTableWidgetItem(f"{i}"))

    def eventFilter(self, source: QWidget, event: QEvent):
        if (event.type() == QEvent.Type.MouseButtonPress and event.buttons() == Qt.MouseButton.RightButton):
            item = self.itemAt(event.pos())
            if item:
                self.__contextMenu.move(self.myParent.pos().x() + self.pos().x() + event.pos().x() + 15, self.myParent.pos().y() + self.pos().y() + event.pos().y() + 40)
                self.__contextMenu.show()
                pass
        elif (event.type() == QEvent.Type.MouseButtonDblClick and event.buttons() == Qt.MouseButton.LeftButton):
            item = self.itemAt(event.pos())
            print(item.text())
        return super(QueuePlaylist, self).eventFilter(source, event)
    
    def menuPressed(self, action: QAction) -> None:
        match action.text():
            case 'Удалить из очереди':
                print("remove from queue")