import logging
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, Qt, QSize
from PyQt5.QtGui import QPalette, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QProgressBar
from threading import Thread

from res import icons
from src.emulators import fceux, zsnes, mupen64plus, dolphin, citra
from ui import ui_window

emulator_count = 5

class MainWindow(QMainWindow, ui_window.Ui_Window):
    emulator_found = QtCore.pyqtSignal(dict)
    emulators_loaded = QtCore.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.emulators = {}

        #Menu actions
        self.actionQuit.triggered.connect(QCoreApplication.quit)

        #Toolbar actions
        self.actionPageEmulation.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        #Other signals
        self.emulator_found.connect(self.add_emulator)
        self.emulators_loaded.connect(self.reset_status)

        #Add a second toolbar on emulation page
        self.toolBarEmulation = QToolBar()
        self.toolBarEmulation.setFloatable(False)
        self.toolBarEmulation.setMovable(False)
        self.toolBarEmulation.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolBarEmulation.setStyleSheet('QToolButton { padding-right: -3px; }')
        self.pageEmulationLayout.addWidget(self.toolBarEmulation, 0, 0)

        #Add progress bar to status bar
        self.taskProgress = QProgressBar()
        self.taskProgress.setVal = lambda x: ( self.taskProgress.setVisible(True), self.taskProgress.setValue(x) )
        self.taskProgress.setVal(0)
        self.taskProgress.setTextVisible(False)
        self.taskProgress.setMaximumHeight(16)
        self.taskProgress.setStyleSheet('margin-right: 8px;')
        self.statusBar.addPermanentWidget(self.taskProgress)

        #Also print messages to terminal
        self.statusBar.showMsg = lambda msg, timeout: ( logging.info(msg), self.statusBar.showMessage(msg, timeout) )

        #Styling
        system_colors = QApplication.palette()
        #The color is close enough to the default border color
        self.setStyleSheet('QToolBar { border-bottom: 1px solid ' + system_colors.color(QPalette.Disabled, QPalette.Button).darker(115).name() + '; }')

    def showEvent(self, ev):
        QMainWindow.showEvent(self, ev)
        self.statusBar.showMsg('Searching for emulators', 1000)
        Thread(target=self.find_emulators).start()

    def change_emulator(self, index):
        current = self.stackedWidgetEmulation.currentIndex()

        if current != index:
            emulator = self.emulators[list(self.emulators.keys())[current]]
            emulator['action'].setIcon(QIcon(emulator['action'].icon().pixmap(QSize(24, 24), QIcon.Disabled)))

            self.stackedWidgetEmulation.setCurrentIndex(index)
            emulator = self.emulators[list(self.emulators.keys())[index]]
            emulator['action'].setIcon(QIcon(':' + emulator['icon']))

    def find_emulators(self):
        #Search for FCEUX
        self.emulator_found.emit(fceux.find())
        #Search for ZSNES
        self.emulator_found.emit(zsnes.find())
        #Search for Mupen64Plus
        self.emulator_found.emit(mupen64plus.find())
        #Search for Dolphin Emulator
        self.emulator_found.emit(dolphin.find())
        #Search for Citra
        self.emulator_found.emit(citra.find())

        self.emulators_loaded.emit()

    def add_emulator(self, emulator):
        if len(emulator['path']) > 0:
            self.statusBar.showMsg('Found ' + emulator['name'], 1000)
        else:
            self.statusBar.showMsg('Failed to find ' + emulator['name'], 1000)

        self.emulators[emulator['name']] = emulator

        i = self.stackedWidgetEmulation.count()
        self.taskProgress.setVal((100 / emulator_count) * (i + 1))

        emulator['action'] = QAction()

        emulator['action'].setIcon(QIcon(':' + emulator['icon']))
        if i > 0:
            self.toolBarEmulation.addSeparator()
            emulator['action'].setIcon(QIcon(emulator['action'].icon().pixmap(QSize(24, 24), QIcon.Disabled)))

        emulator['action'].setIconText(emulator['name'])
        emulator['action'].triggered.connect(lambda checked, index=i: self.change_emulator(index))

        self.toolBarEmulation.addAction(emulator['action'])
        self.stackedWidgetEmulation.insertWidget(i, emulator['widget'](emulator))

        if len(emulator['path']) == 0:
            self.toolBarEmulation.widgetForAction(emulator['action']).setStyleSheet('color: ' + QApplication.palette().color(QPalette.Disabled, QPalette.WindowText).name() + ';')

    def reset_status(self):
        self.statusBar.clearMessage()
        self.taskProgress.setValue(0)
        self.taskProgress.setVisible(False)
