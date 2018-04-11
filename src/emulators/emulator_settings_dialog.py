from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog

from ui import ui_emulator_settings

class EmulatorSettingsDialog(QDialog, ui_emulator_settings.Ui_EmulatorSettings):
    def __init__(self, parent, data):
        super(EmulatorSettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.data = data

        self.settings = QSettings('SanderTheDragon', 'Qtendo')
        self.settings_prefix = 'emulation/emulator/' + self.data['name'].lower().replace(' ', '_')

        self.cancelButton.pressed.connect(lambda: self.reject())
        self.acceptButton.pressed.connect(lambda: self.save())
        self.commandFormat.textChanged.connect(lambda: self.show_preview())

        self.commandFormat.setText(self.settings.value(self.settings_prefix + '/command', '{EXEC} {ARGS} {ROM}', type=str))

    def show_preview(self):
        command = self.commandFormat.text()
        command = command.replace('{EXEC}', self.data['path'])
        command = command.replace('{ARGS}', ' '.join(self.data['arguments']))
        command = command.replace('{ROM}', '/rom' + self.data['platforms'][list(self.data['platforms'].keys())[0]][0])
        self.commandFormatPreview.setText(command)

    def save(self):
        self.settings.setValue(self.settings_prefix + '/command', self.commandFormat.text())

        self.accept()
