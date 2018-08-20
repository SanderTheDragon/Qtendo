#!/usr/bin/python3

import logging
import os
import sys
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication

from src import main_window

def setup_logging():
    formatter = '[%(asctime)s %(filename)s %(levelname)s] %(message)s'
    log_level = logging.DEBUG

    #Log to file
    directory = os.path.dirname(QSettings('SanderTheDragon', 'Qtendo').fileName())
    if not os.path.isdir(directory):
        os.makedirs(directory)

    logging.basicConfig(filename=os.path.join(directory, 'qtendo.log'), filemode='w', format=formatter, level=log_level)

    #Also log to terminal
    terminal_logging = logging.StreamHandler()
    terminal_logging.setLevel(log_level)
    terminal_logging.setFormatter(logging.Formatter(formatter))
    logging.getLogger().addHandler(terminal_logging)



if __name__ == '__main__':
    setup_logging()

    logging.info('Starting Qtendo')

    app = QApplication(sys.argv)
    window = main_window.MainWindow()
    window.show()
    return_code = app.exec_()
    if return_code != 0:
        logging.error('Something went wrong')

    logging.info('Shutting down Qtendo')

    logging.info('Bye')
    sys.exit(return_code)
