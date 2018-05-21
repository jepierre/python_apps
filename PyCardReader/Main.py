# -*- coding: utf-8 -*-
""""
Author: Jean Pierre
Last Edited: 05/20/2018

"""

__appname__ = 'PyCardReader'
__module__ = 'main'


# Import modules
import logging
import sys
import os
import re
from PyQt5 import (uic)
from PyQt5.QtWidgets import (QApplication, QLabel, QSplashScreen, QMainWindow, QTableWidgetItem,
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import (QTime, QTimer, Qt, QThread, pyqtSignal, QSettings, QCoreApplication)
from PyQt5.QtGui import (QPixmap)
import pytesseract

# Sets up path
app_data_path = os.path.dirname(__file__)

# Set up logging
logging.basicConfig(filename=app_data_path + r'\pycardreader.log',
                    format='%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)\
                    -6d -%(message)s')
logger = logging.getLogger(name='main-gui')
logger.setLevel(logging.DEBUG)


class Main(QMainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        uic.loadUi(r'ui_files\main.ui', self)
        logger.debug('loading main.ui')
        self.setWindowTitle(__appname__)
        self.init_ui()

        self.show()

    def init_ui(self):
        self.action_open.triggered.connect(self.open_file)
        self.action_save.triggered.connect(self.save_file)
        self.action_exit.triggered.connect(self.exit_app)

    def open_file(self):
        self.open_file_name = QFileDialog.getOpenFileName(self, "Open Image", app_data_path + r'\images', 'All files (*.*)')[0]
        logger.debug(f'open_file_name: {self.open_file_name}')

        pixmap = QPixmap(self.open_file_name)
        self.label_input_img.setPixmap(pixmap)

    def save_file(self):
        self.save_file_name = QFileDialog.getSaveFileName(self, "Save Result", app_data_path + r'\result', "All files (*.*)")[0]
        logger.debug(f'save_file_name: {self.save_file_name}')

    def exit_app(self):
        sys.exit(0)


def main():
    os.chdir(os.path.dirname(__file__))
    QCoreApplication.setApplicationName('PyCardReader')
    QCoreApplication.setApplicationVersion('0.1')
    QCoreApplication.setOrganizationName('PyCardReader')
    QCoreApplication.setOrganizationDomain('pycardreader.com')

    # Enable logging on the console
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)\
                    -6d -%(message)s'))
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # Opens the app
    app = QApplication(sys.argv)
    App = Main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
