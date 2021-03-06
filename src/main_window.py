import logging
from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray, QCoreApplication, QSettings, QSize, Qt
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QProgressBar, QToolBar
from threading import Thread

from res import icons
from src.dialogs import about, settings
from src.emulators import citra, dolphin, fceux, mupen64plus, zsnes
from ui import ui_window

emulator_count = 5

class MainWindow(QMainWindow, ui_window.Ui_Window):
    emulator_found = QtCore.pyqtSignal(dict)
    emulators_loaded = QtCore.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.emulators = { }

        self.settings = QSettings('SanderTheDragon', 'Qtendo')

        self.ui_create()
        self.ui_connect()
        self.settings_load()



    def showEvent(self, ev):
        QMainWindow.showEvent(self, ev)

        self.statusBar.showMsg('Searching for emulators', 1000)
        Thread(target=self.find_emulators, daemon=True).start()


    def closeEvent(self, ev):
        QMainWindow.closeEvent(self, ev)

        self.settings_save()



    def ui_create(self):
        #Add toolbar
        self.toolBar = QToolBar()
        self.toolBar.addAction(self.actionPageEmulation)
        self.toolBar.setFloatable(False)
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.gridLayout.addWidget(self.toolBar, 1, 0)

        #Add a second toolbar on emulation page
        self.toolBarEmulation = QToolBar()
        self.toolBarEmulation.setFloatable(False)
        self.toolBarEmulation.setMovable(False)
        self.toolBarEmulation.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.pageEmulationLayout.addWidget(self.toolBarEmulation, 0, 0)

        #Add progress bar to status bar
        self.taskProgress = QProgressBar()
        self.taskProgress.setVal = lambda x: ( self.taskProgress.setVisible(True), self.taskProgress.setValue(x) )
        self.taskProgress.setVal(0)
        self.taskProgress.setTextVisible(False)
        self.statusBar.addPermanentWidget(self.taskProgress)

        #Also print messages to terminal
        self.statusBar.showMsg = lambda msg, timeout: ( logging.info(msg), self.statusBar.showMessage(msg, timeout) )

        #Styling
        self.setStyleSheet('QToolButton { padding-right: -3px; }')


    def ui_connect(self):
        #Menu actions
        self.actionQuit.triggered.connect(QCoreApplication.quit)
        self.actionSettings.triggered.connect(lambda: settings.SettingsDialog(parent=self).exec_())
        self.actionAbout.triggered.connect(lambda: about.AboutDialog(parent=self).exec_())

        #Toolbar actions
        self.actionPageEmulation.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        #Other signals
        self.emulator_found.connect(self.add_emulator)
        self.emulators_loaded.connect(self.reset_status)


    def settings_load(self):
        if self.settings.value('qtendo/window/restore', True, type=bool):
            self.restoreGeometry(self.settings.value('qtendo/window/geometry', type=QByteArray))


    def settings_save(self):
        if self.settings.value('qtendo/window/restore', True, type=bool):
            self.settings.setValue('qtendo/window/geometry', self.saveGeometry())



    def change_emulator(self, index):
        current = self.stackedWidgetEmulation.currentIndex()

        if current != index:
            emulator = self.emulators[list(self.emulators.keys())[current]]
            emulator['action'].setIcon(QIcon(emulator['action'].icon().pixmap(QSize(24, 24), QIcon.Disabled)))

            self.stackedWidgetEmulation.setCurrentIndex(index)
            emulator = self.emulators[list(self.emulators.keys())[index]]
            emulator['action'].setIcon(QIcon(':' + emulator['icon']))


    def add_emulator(self, emulator):
        if len(emulator['path']) > 0:
            self.statusBar.showMsg('Found ' + emulator['name'], 1000)
        else:
            self.statusBar.showMsg('Failed to find ' + emulator['name'], 1000)

        self.emulators[emulator['name']] = emulator

        i = self.stackedWidgetEmulation.count()
        emulator['action'] = QAction()

        emulator['action'].setIcon(QIcon(':' + emulator['icon']))
        if i > 0:
            self.toolBarEmulation.addSeparator()
            emulator['action'].setIcon(QIcon(emulator['action'].icon().pixmap(QSize(24, 24), QIcon.Disabled)))

        emulator['action'].setIconText(emulator['name'])
        emulator['action'].triggered.connect(lambda checked, index=i: self.change_emulator(index))

        self.toolBarEmulation.addAction(emulator['action'])
        self.stackedWidgetEmulation.insertWidget(i, emulator['widget'](emulator))

        if len(self.settings.value('emulation/emulator/' + emulator['name'].lower().replace(' ', '_') + '/path', emulator['path'], type=str)) == 0:
            self.toolBarEmulation.widgetForAction(emulator['action']).setStyleSheet('color: ' + QApplication.palette().color(QPalette.Disabled, QPalette.WindowText).name() + ';')

        emulator['reload_settings'] = self.reload_settings

        self.taskProgress.setVal(int((100.0 / float(emulator_count)) * float(i + 1)))


    def reset_status(self):
        self.statusBar.clearMessage()
        self.taskProgress.setValue(0)
        self.taskProgress.setVisible(False)


    def reload_settings(self):
        emulator = self.emulators[list(self.emulators.keys())[self.stackedWidgetEmulation.currentIndex()]]

        if len(self.settings.value('emulation/emulator/' + emulator['name'].lower().replace(' ', '_') + '/path', emulator['path'], type=str)) == 0:
            self.toolBarEmulation.widgetForAction(emulator['action']).setStyleSheet('color: ' + QApplication.palette().color(QPalette.Disabled, QPalette.WindowText).name() + ';')
        else:
            self.toolBarEmulation.widgetForAction(emulator['action']).setStyleSheet('')



    def find_emulators(self):
        #Search for FCEUX
        self.emulator_found.emit(fceux.find(None if not self.settings.contains('emulation/emulator/fceux/path') else self.settings.value('emulation/emulator/fceux/path', type=str)))
        #Search for ZSNES
        self.emulator_found.emit(zsnes.find(None if not self.settings.contains('emulation/emulator/zsnes/path') else self.settings.value('emulation/emulator/zsnes/path', type=str)))
        #Search for Mupen64Plus
        self.emulator_found.emit(mupen64plus.find(None if not self.settings.contains('emulation/emulator/mupen64plus/path') else self.settings.value('emulation/emulator/mupen64plus/path', type=str)))
        #Search for Dolphin Emulator
        self.emulator_found.emit(dolphin.find(None if not self.settings.contains('emulation/emulator/dolphin/path') else self.settings.value('emulation/emulator/dolphin/path', type=str)))
        #Search for Citra
        self.emulator_found.emit(citra.find(None if not self.settings.contains('emulation/emulator/citra/path') else self.settings.value('emulation/emulator/citra/path', type=str)))

        self.emulators_loaded.emit()
