from PyQt5.QtCore import QCoreApplication, Qt, QSize
from PyQt5.QtGui import QPalette, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction

from ui import ui_window
from res import icons

class MainWindow(QMainWindow, ui_window.Ui_Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        #Menu actions
        self.actionQuit.triggered.connect(QCoreApplication.quit)

        #Toolbar actions
        self.actionPageEmulation.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        #Add a second toolbar on emulation page
        self.toolBarEmulation = QToolBar()
        self.toolBarEmulation.setFloatable(False)
        self.toolBarEmulation.setMovable(False)
        self.toolBarEmulation.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolBarEmulation.setStyleSheet('QToolButton { padding-right: -3px; }')
        self.pageEmulationLayout.addWidget(self.toolBarEmulation, 0, 0)

        #Styling
        system_colors = QApplication.palette()
        #The color is close enough to the default border color
        self.setStyleSheet('QToolBar { border-bottom: 1px solid ' + system_colors.color(QPalette.Disabled, QPalette.Button).darker(115).name() + '; }')

    def change_emulator(self, index):
        current = self.stackedWidgetEmulation.currentIndex()

        if current != index:
            emulator = self.emulators[list(self.emulators.keys())[current]]
            emulator['action'].setIcon(QIcon(emulator['action'].icon().pixmap(QSize(24, 24), QIcon.Disabled)))

            self.stackedWidgetEmulation.setCurrentIndex(index)
            emulator = self.emulators[list(self.emulators.keys())[index]]
            emulator['action'].setIcon(QIcon(':' + emulator['icon']))

    def set_emulators(self, emulators):
        self.emulators = emulators

        for i in range(len(self.emulators.keys())):
            emulator = self.emulators[list(emulators.keys())[i]]
            emulator['action'] = QAction()

            emulator['action'].setIcon(QIcon(':' + emulator['icon']))
            if i > 0:
                emulator['action'].setIcon(QIcon(emulator['action'].icon().pixmap(QSize(24, 24), QIcon.Disabled)))

            emulator['action'].setIconText(emulator['name'])
            emulator['action'].triggered.connect(lambda checked, index=i: self.change_emulator(index))

            self.toolBarEmulation.addAction(emulator['action'])
            self.stackedWidgetEmulation.insertWidget(i, emulator['widget'](emulator))

            if len(emulator['path']) == 0:
                self.toolBarEmulation.widgetForAction(emulator['action']).setStyleSheet('color: ' + QApplication.palette().color(QPalette.Disabled, QPalette.WindowText).name() + ';')

            if i + 1 < len(emulators.keys()):
                self.toolBarEmulation.addSeparator()
