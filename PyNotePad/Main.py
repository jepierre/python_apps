# -*- coding: utf-8 -*-
""" 
    PyNotePad App
"""
__appname__ = "PyNotePad"

import logging
import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.Qt import QFontDatabase
import termcolor
import traceback

app_path = os.path.dirname(__file__)
__path__ = app_path
app_log_path = os.path.join(app_path, "logs")

if not os.path.exists(app_log_path):
    os.makedirs(app_log_path)

log_file_name = __appname__ + ".txt"

formatter = "%(asctime)s: %(name)s -%(levelname)s -%(module)s -%(funcName)s -%(lineno)-3d -%(message)s"
logging.basicConfig(
    filename=os.path.join(app_log_path, log_file_name), format=formatter
)
logger = logging.getLogger(name="main-gui")
logger.setLevel(logging.DEBUG)


class Main(QMainWindow):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        uic.loadUi(r"ui_files/main.ui", self)
        logger.debug("loading main.ui")
        self.setWindowTitle(__appname__)
        self.init_ui()

        self.show()

    def init_ui(self):
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixed_font.setPointSize(12)
        self.main_text_edit.setFont(fixed_font)
        self.action_exit.triggered.connect(self.exit_app)

    def exit_app(self):
        sys.exit(0)

    def save_file(self):
        pass

    def save_file_as(self):
        pass

    def open_file(self):
        pass


def main():
    # make sure were in the current path of the Main file
    os.chdir(os.path.dirname(__file__))

    # Enable logging on the console
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(formatter))
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # catches errors in gui and print them
    def excepthook(etype, value, tb):
        if isinstance(value, KeyboardInterrupt):
            sys.exit(1)
        else:
            termcolor.cprint("Sorry, something's wrong! ", "yellow", file=sys.stderr)
            # print traceback
            traceback.print_exception(etype, value, tb)

    # Set global exception handler.
    sys.excepthook = excepthook

    # Open the app
    app = QApplication(sys.argv)
    App = Main(parent=None)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
