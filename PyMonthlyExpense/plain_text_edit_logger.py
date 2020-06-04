# -*- coding: utf-8 -*-
""""
Author: Jean Pierre
Last Edited:

https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt/35593078#35593078
"""
import logging

from PyQt5 import uic, Qt, QtCore
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (
    QPlainTextEdit,
    QWidget,
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QDockWidget,
    QTextEdit,
    QGroupBox,
)
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter(
    "%(asctime)s: %(name)s - %(levelname)s - <%(module)s:%(funcName)s:%(lineno)d> - %(message)s"
)


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, text_box_handle):
        logging.Handler.__init__(self)
        self.text_edit_logger = text_box_handle
        self.text_edit_logger.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.text_edit_logger.append(msg)
        self.text_edit_logger.moveCursor(QTextCursor.End)

    def write(self, m):
        pass


class CustomLoggerWidget(QDockWidget):
    def __init__(self, formatter=FORMATTER):
        super().__init__()
        self.setWindowTitle("Log")
        self.formatter = formatter
        self.init_ui()

    def init_ui(self):
        text_box_handle = QTextEdit()
        text_box_handle.document().setDefaultStyleSheet(
            ".CRITICAL{color:red; font-weight:bold} .ERROR{color:#CC0000; weight:bold} "
            ".WARNING{color:#CCAA33} .INFO{color:black} .DEBUG{color:green} .VERBOSE{color:blue} "
            ".TIME{color:black} .MODULE{color:purple} .FUNCTION {color:gray; font-weight:bold}"
        )
        text_box_handle.append("<style>.DEBUG {color:red} .INFO {color:blue} </style>")
        formatter = logging.Formatter(
            fmt="<span class=TIME>%(asctime)s </span>"
            + "<span class=MODULE>&lt;%(module)s&gt; </span>"
            + "<span class=FUNCTION>&lt;%(funcName)s:%(lineno)s&gt;</span>"
            + "<span class=%(levelname)s> %(levelname)s - %(message)s</span>"
        )
        # text_box_handle.document().setDefaultStyleSheet('.CRITICAL{color:red; font-weight:bold}'
        #                                                 '.ERROR{color:#cc000; weight:bold}'
        #                                                 '.WARNING{color:#CCAA33} .INFO{color:black}')
        # text_box_handle.append('<style>.DEBUG {color:red} .INFO{color:blue} </style>')
        # formatter = logging.Formatter(fmt='<span class=TIME>%(asctime)s </span>' +
        #                                   '<span class=MODULE>&lt;%(module)s&gt; </span>')

        log_text_box = QPlainTextEditLogger(text_box_handle)

        # set format
        log_text_box.setFormatter(formatter)
        logging.getLogger().addHandler(log_text_box)

        # set logging level
        logging.getLogger().setLevel(logging.DEBUG)

        # vboxformat.addWidget(log_text_box.text_edit_logger)
        # vboxformat.addWidget(text_box_handle)
        self.setWidget(text_box_handle)
        # self.dock_log.setWidget(text_box_handle)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Logger Example")
        self.setGeometry(200, 200, 640, 480)
        self._button = QPushButton()
        self._button.setText("Test Me")

        group_box = QGroupBox()
        layout = QVBoxLayout()
        layout.addWidget(self._button)
        te = QTextEdit()
        logg = QPlainTextEditLogger(te)

        clogger = CustomLoggerWidget(self)
        # layout.addWidget(clogger)
        # layout.addWidget(logg.text_edit_logger)

        self._button.clicked.connect(self.test)

        group_box.setLayout(layout)
        # self.setCentralWidget(QTextEdit())
        self.layout().addWidget(group_box)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, clogger)
        # self.layout().addWidget(self._button)

        self.show()

    def test(self):
        logging.debug("damn, a bug")
        logging.info("something to remember")
        logging.warning("that's not right")
        logging.error("foobar")


def main():

    # Enable logging on the console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(FORMATTER)
    logger.addHandler(ch)

    # Opens the app
    app = QApplication(sys.argv)
    App = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
