from PyQt5.QtCore import QDir, QSettings
from PyQt5.QtWidgets import QDialog, QFileDialog

from ui import ui_settings

class SettingsDialog(QDialog, ui_settings.Ui_Settings):
    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)

        self.settings = QSettings('SanderTheDragon', 'Qtendo')

        self.cancelButton.pressed.connect(lambda: self.reject())
        self.acceptButton.pressed.connect(lambda: self.save())

        #General
        self.windowCheckboxGeometry.setChecked(self.settings.value('qtendo/window/restore', True, type=bool))

        #Emulation
        self.pathList.addItems(self.settings.value('emulation/roms/paths', [ QDir.homePath() ], type=str))
        self.pathList.itemSelectionChanged.connect(lambda: self.removePathButton.setEnabled(len(self.pathList.selectedItems()) > 0))
        self.addPathButton.pressed.connect(lambda: self.pathList.addItem(QFileDialog.getExistingDirectory(self, 'Add ROM directory', QDir.homePath(), QFileDialog.ShowDirsOnly)))
        self.removePathButton.pressed.connect(lambda: self.pathList.takeItem(self.pathList.row(self.pathList.selectedItems()[0])))


    def save(self):
        #General
        self.settings.setValue('qtendo/window/restore', self.windowCheckboxGeometry.isChecked())

        #Emulation
        paths = []
        for i in range(self.pathList.count()):
            paths.append(self.pathList.item(i).text())
        self.settings.setValue('emulation/roms/paths', paths)

        self.accept()
