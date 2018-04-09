#!/usr/bin/python3

import logging
import sys
from PyQt5.QtWidgets import QApplication

from src import main_window, utils

if __name__ == '__main__':
    utils.setup_logging()

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
