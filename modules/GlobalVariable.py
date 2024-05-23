from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
import sys, os

app = QApplication(sys.argv)

APP_ICON = QPixmap(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\app.png').scaled(25,25,transformMode=Qt.TransformationMode.SmoothTransformation)
CLOSE_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\close.png')
MINIMIZE_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\minimize.png')
PLAY_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\play.png')
PAUSE_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\pause.png')
PREVIOUS_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\previous.png')
NEXT_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\next.png')

CSS = '''
    * {
        color: rgb(240,240,240);
        font-size: 14px;
    }
    #TitleBar {
        background-color: rgb(21,21,21);
    }
    #MainWindow {
        background-color: rgb(40,40,40);
        border: 1px solid rgb(21,21,21);
    }


    #btn_red_transp {
        background-color: rgba(200,0,0,0);
        border: 0px;
    }
    #btn_red_transp:hover {
        background-color: rgba(200,0,0,0.3)
    }
    #btn_red_transp:pressed {
        background-color: rgba(200,0,0,0.6);
    }
    #btn_orange_transp {
        background-color: rgba(255,88,0,0);
        border: 0px;
    }
    #btn_orange_transp:hover {
        background-color: rgba(255,88,0,0.3);
    }
    #btn_orange_transp:pressed {
        background-color: rgba(255,88,0,0.6);
    }
    #btn_orange {
        background-color: rgba(255,88,0,0.8);
        border: 1px solid rgb(0,0,0);
        border-radius: 15px;
    }
    #btn_orange:hover {
        background-color: rgba(255,88,0,0.6);
    }
    #btn_orange:pressed {
        background-color: rgba(255,88,0,0.4);
    }
    #btn_red {
        background-color: rgba(200,0,0,0.8);
        border: 1px solid rgb(0,0,0);
        border-radius: 15px;
    }
    #btn_red:hover {
        background-color: rgba(200,0,0,0.6);
    }
    #btn_red:hover {
        background-color: rgba(200,0,0,0.4);
    }

    QHeaderView {
        background-color: rgba(0,0,0,0);
    }
    QHeaderView::section {
        background-color: rgba(0,0,0,0);
        border: 1px solid rgb(21,21,21);
        font: bold;
        padding-left: 5px;
    }
    #tablePlaylist {
        background-color: rgba(0,0,0,0);
        border: none;
    }
    QScrollBar:vertical {
        background-color: rgba(0,0,0,0);
        width: 7px;
    }
    QScrollBar::handle:vertical {
        background-color: rgba(255,88,0,1);
        border: 1px solid rgb(21,21,21);
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background-color: rgb(21,21,21);
    }
    QTableView::item:selected {
        background: rgba(21,21,21,0.5);
        color: rgb(240,240,240);
        border: none;
    }
'''