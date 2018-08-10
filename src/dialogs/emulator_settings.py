import mimetypes
import os
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog

from src import syntax
from ui import ui_emulator_settings

class EmulatorSettingsDialog(QDialog, ui_emulator_settings.Ui_EmulatorSettings):
    def __init__(self, parent, data):
        super(EmulatorSettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.data = data

        self.settings = QSettings('SanderTheDragon', 'Qtendo')
        self.settings_prefix = 'emulation/emulator/' + self.data['name'].lower().replace(' ', '_')

        self.parent().create_settings_ui(self)
        self.ui_connect()



    def ui_connect(self):
        self.cancelButton.pressed.connect(lambda: self.reject())
        self.acceptButton.pressed.connect(lambda: self.settings_save())

        #General
        self.pathEdit.textChanged.connect(lambda: ( self.check_path(), self.show_preview() ))
        self.pathEdit.setText(self.settings.value(self.settings_prefix + '/path', self.data['path'], type=str))

        self.commandFormat.textChanged.connect(lambda: self.show_preview())
        self.commandFormat.setText(self.settings.value(self.settings_prefix + '/command', '{EXEC} {ARGS} {ROM}', type=str))

        #File edit
        self.fileSelect.currentTextChanged.connect(lambda file: self.change_file(file))
        self.fileSaveButton.pressed.connect(lambda: self.save_file())


    def settings_save(self):
        self.settings.setValue(self.settings_prefix + '/command', self.commandFormat.text())

        exec_path = self.settings.value(self.settings_prefix + '/path', self.data['path'], type=str)
        if self.pathEdit.text() != exec_path and os.path.isfile(self.pathEdit.text()):
            exec_path = self.pathEdit.text()
        if len(self.pathEdit.text()) == 0:
            exec_path = self.data['path']
        self.settings.setValue(self.settings_prefix + '/path', exec_path)

        self.accept()



    def show_preview(self):
        command = self.commandFormat.text()
        exec_path = self.settings.value(self.settings_prefix + '/path', self.data['path'], type=str)
        if self.pathEdit.text() != exec_path and os.path.isfile(self.pathEdit.text()):
            exec_path = self.pathEdit.text()
        if len(exec_path) == 0:
            exec_path = self.data['name'].lower().replace(' ', '-')

        command = command.replace('{EXEC}', exec_path)
        command = command.replace('{ARGS}', ' '.join(self.data['arguments']))
        command = command.replace('{ROM}', '/rom' + self.data['platforms'][list(self.data['platforms'].keys())[0]][0])
        self.commandFormatPreview.setText(command)


    def check_path(self):
        self.pathEdit.setStyleSheet('color: ' + ('green' if os.path.isfile(self.pathEdit.text()) else 'red') + ';')



    def change_file(self, file):
        with open(file, 'r') as stream:
            self.fileTextEdit.setText(stream.read())

        if self.parent().get_config_format() == 'ini':
            self.highlighter = syntax.IniHighlighter(self.fileTextEdit.document())


    def save_file(self):
        with open(self.fileSelect.currentText(), 'w') as stream:
            stream.write(self.fileTextEdit.toPlainText())
