# -*- coding: utf-8 -*-
""""
Author: Jean Pierre
Last Edited: 05/19/2018

calculator.py
http://zetcode.com/gui/pyqt5/layout/
"""
__appname__ = "TabExample"


# Import Modules
import sys
import os
import logging
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QApplication,
    QMainWindow,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QGroupBox,
    QSpacerItem,
    QSizePolicy,
    QTextEdit,
)
from PyQt5.QtCore import Qt

# Setup Logging
logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)


class TabExample(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

        self.setWindowTitle(__appname__)
        self.show()

    def init_ui(self):
        self.centra_widget = QWidget()

    def update_ui(self, button):
        pass


def main():
    # add stream handler logger
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # sets up path
    __path__ = os.path.dirname(__file__)
    os.chdir(__path__)

    # loads app
    app = QApplication(sys.argv)
    tab_example = TabExample()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
