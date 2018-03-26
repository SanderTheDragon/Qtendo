#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import ui_window

class MainWindow(QMainWindow, ui_window.Ui_Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
