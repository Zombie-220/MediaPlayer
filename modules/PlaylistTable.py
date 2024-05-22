from PyQt6.QtWidgets import QMainWindow, QTableWidget, QAbstractItemView, QTableWidgetItem
from PyQt6.QtCore import Qt, QEvent
import os, eyed3
import threading

class PlaylistTable(QTableWidget):
    def __init__(self, parent: QMainWindow):
        super().__init__(0, 3, parent)

        self.setObjectName("tablePlaylist")
        self.setFixedSize(parent.width()-2, parent.height()-31)
        self.move(1,30)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setColumnWidth(0, (((parent.width()-110) * 50) // 100))
        self.setColumnWidth(1, (((parent.width()-110) * 50) // 100))
        self.setColumnWidth(2, 108)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignBottom)
        self.setHorizontalHeaderLabels(["Название", "Исполнтель", "Длительность"])
        self.cellDoubleClicked.connect(self.dblClickEvent)
        self.viewport().installEventFilter(self)
        
        path = R'C:\Users\Zombie\Desktop\по мелочи\music'
        self.loadPlaylistThread = threading.Thread(target=lambda:[self.loadPlaylist(path)])

    def loadPlaylist(self, path: str) -> None:
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
                        self.setSpan(self.rowCount()-1, 0, 1, 2)
                        self.setItem(self.rowCount()-1, 0, QTableWidgetItem(f'{file}'))
                        duration = "--:--"
                    self.setItem(self.rowCount()-1, 2, QTableWidgetItem(duration))

    def dblClickEvent(self, row, column) -> None:
        print(f'double click: {row}')

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.RightButton:
                print("rightBtn")
        # elif event.type() == QEvent.Type.MouseButtonDblClick:
        #     if event.button() == Qt.MouseButton.LeftButton:
        #         print("leftBtn x2")
        #     elif event.button() == Qt.MouseButton.RightButton:
        #         print("rightBtn x2")
        return super().eventFilter(source, event)