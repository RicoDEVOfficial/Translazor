import json, os
from PyQt5 import QtWidgets
import qdarkstyle
from Others.gui import LoginWindow, MainWindow
import os, sys
# make script’s folder the current working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# load config
with open(os.path.join(os.path.dirname(__file__), 'NetStuff/config.json')) as f:
    cfg = json.load(f)

def main():
    app = QtWidgets.QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    login = LoginWindow()
    mainwin = MainWindow()
    login.switch_to_main.connect(lambda: (login.close(), mainwin.show()))
    login.show()
    app.exec_()

if __name__ == '__main__':
    main()