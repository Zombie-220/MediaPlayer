from PyQt6.QtWidgets import QMainWindow, QTableWidget, QAbstractItemView, QTableWidgetItem
from PyQt6.QtCore import Qt
import os, eyed3

from modules.GlobalVariable import CSS

class PlaylistTable(QTableWidget):
    def __init__(self, parent: QMainWindow):
        super().__init__(0, 3, parent)