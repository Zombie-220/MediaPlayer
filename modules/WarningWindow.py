from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

import os, threading, sqlite3

from modules.SimpleModules import WindowTitleBar, Label, Button
from modules.GlobalVariable import WARNING_ICON, WARNING_WINDOW_CSS

from MainWindowHeader import MainWindow

class WarningWindow(QMainWindow):
    def __init__(self, mediaWindow: MainWindow):
        super().__init__()
        self.icon = WARNING_ICON
        self.title = "Ой-ой, что-то пошло не так"
        self.__mediaWindow = mediaWindow

        self.setFixedSize(450, 200)
        self.setWindowIcon(QIcon(WARNING_ICON))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet(WARNING_WINDOW_CSS)
        self.setObjectName("WarningWindow")

        windowHat = WindowTitleBar(self, self.icon, self.title, "WarningWindowTitle")

        label = Label(self, (self.width()//2)-150, windowHat.height()+25, 300, 55, "label", "Выбранный путь не имеет .mp3 файлов\nБудь внимателен при выборе пути, самурай")
        btn_cancel = Button(self, "Отмена", (self.width()//2)-150-20, label.pos().y()+label.height()+25, 150, 30, "btn", self.cancel)
        btn_retry = Button(self, "Выбрать путь...", (self.width()//2)+20, label.pos().y()+label.height()+25, 150, 30, "btn", self.retry)

        # self.returnedVariable = None

    def cancel(self) -> None:
        self.__mediaWindow.setDisabled(False)
        self.close()

    def retry(self) -> str:
        self.__mediaWindow.buttonInterface.stop()
        newPath = QFileDialog.getExistingDirectory(directory=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        dirHasMP3 = False
        for root, dirs, files in os.walk(newPath):
            for file in files:
                if file.endswith(".mp3"):
                    dirHasMP3 = True
                    break
            break

        if dirHasMP3:
            self.close()
            self.__mediaWindow.playlist.path = newPath
            loadListThread = threading.Thread(target=lambda:[self.__mediaWindow.playlist.loadPlaylist(self.__mediaWindow.playlist.path)])
            loadListThread.start()

            connect = sqlite3.connect("database.db")
            cursor = connect.cursor()
            
            cursor.execute("UPDATE pathToDir SET path=?", (newPath,))

            connect.commit()
            connect.close()
            self.__mediaWindow.setDisabled(False)