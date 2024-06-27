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
REDUCE_VOLUME_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\reduceVolume.png')
ADD_VOLUME_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\addVolume.png')
MUTE_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\mute.png')
REPEAT_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\repeat.png')
RANDOM_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\random.png')
WARNING_ICON = QPixmap(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\warning.png').scaled(25,25,transformMode=Qt.TransformationMode.SmoothTransformation)
FOLDER_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\folder.png')
MINI_WINDOW_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\miniWindow.png')
DOTS_ICON = QPixmap(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\dots.png').scaled(15,15,transformMode=Qt.TransformationMode.SmoothTransformation)
FULLSCREEN_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\fullscreen.png')

CSS = '''
    * {
        color: rgb(240,240,240);
        font-size: 14px;
    }
    #MainWindow, #border-comp, QToolTip {
        background-color: rgb(40,40,40);
        border: 1px solid rgb(21,21,21);
    }
    #dark-comp {
        background-color: rgb(21,21,21);
        border: none;
    }
    #dark-comp-radius {
        background-color: rgb(21,21,21);
        border: none;
        border-radius: 15px;
    }
    #transp-comp {
        background-color: rgba(0,0,0,0);
        border: none;
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

    #btn_red {
        background-color: rgba(200,0,0,0.8);
        border: 1px solid rgb(0,0,0);
        border-radius: 15px;
    }
    #btn_red:hover {
        background-color: rgba(200,0,0,0.6);
    }
    #btn_red:pressed {
        background-color: rgba(200,0,0,0.4);
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



    QToolTip {
        font-size: 12px;
    }
    QSlider:groove {
        border: 1px solid rgb(21,21,21);
        border-radius: 5px;
    }
    QSlider:handle {
        background-color: rgb(255,88,0);
        border-radius: 3px;
        width: 6px;
    }
'''