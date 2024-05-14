from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QAbstractItemView, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import sys, os, eyed3

from modules.GlobalVariable import *
from modules.SimpleModules import WindowTitleBar, Button

# from modules.PlaylistTable import PlaylistTable

class MainWindow(QMainWindow):
    def __init__(self, title: str):
        super().__init__()
        self.icon = APP_ICON
        self.title = title

        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle(self.title)
        self.setStyleSheet(CSS)
        self.setObjectName("MainWindow")
        self.setFixedSize(720, 560)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        windowHat = WindowTitleBar(self)
        btn_close = Button(self, CLOSE_ICON, self.width()-30, 0, 30, 30, "btn_red_transp", self.closeEvent)
        btn_showMinimize = Button(self, MINIMIZE_ICON, self.width()-60, 0, 30, 30, "btn_orange_transp", self.showMinimized)

        self.__table_Playlist = QTableWidget(0, 3, self)
        self.__table_Playlist.setObjectName("tablePlaylist")
        self.__table_Playlist.setFixedSize(self.width()-2, self.height()-31)
        self.__table_Playlist.move(1,30)
        self.__table_Playlist.verticalHeader().setVisible(False)
        self.__table_Playlist.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.__table_Playlist.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.__table_Playlist.setColumnWidth(0, (((self.width()-110) * 50) // 100))
        self.__table_Playlist.setColumnWidth(1, (((self.width()-110) * 50) // 100))
        self.__table_Playlist.setColumnWidth(2, 108)
        self.__table_Playlist.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__table_Playlist.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignBottom)
        self.__table_Playlist.setHorizontalHeaderLabels(["Название", "Исполнтель", "Длительность"])

        self.loadPlaylist(path)

    def loadPlaylist(self, path: str) -> None:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.mp3'):
                    mp3 = eyed3.load(f"{path}\{file}")

                    self.__table_Playlist.insertRow(self.__table_Playlist.rowCount())
                    if mp3.tag.title != None and mp3.tag.artist != None:
                        self.__table_Playlist.setItem(self.__table_Playlist.rowCount()-1, 0, QTableWidgetItem(mp3.tag.title))
                        self.__table_Playlist.setItem(self.__table_Playlist.rowCount()-1, 1, QTableWidgetItem(mp3.tag.artist))
                        duration = f"{int(mp3.info.time_secs//60):02}:{int(mp3.info.time_secs%60):02}"
                    else:
                        self.__table_Playlist.setSpan(self.__table_Playlist.rowCount()-1, 0, 1, 2)
                        self.__table_Playlist.setItem(self.__table_Playlist.rowCount()-1, 0, QTableWidgetItem(f'{file}'))
                        duration = "--:--"
                    self.__table_Playlist.setItem(self.__table_Playlist.rowCount()-1, 2, QTableWidgetItem(duration))

    def closeEvent(self, event) -> None:
        self.close()

if __name__ == '__main__':
    path = R'C:\Users\Zombie\Desktop\по мелочи\music'
    app = QApplication(sys.argv)
    window = MainWindow("Media player")
    window.show()
    sys.exit(app.exec())