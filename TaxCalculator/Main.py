#-*- coding: utf-8 -*-
"""
TaxCalculator
"""
import traceback

import termcolor

__appname__ = "Starter"

import logging
import os
import sys
from PyQt5 import (uic)
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from decimal import Decimal

app_path = os.path.dirname(__file__)
app_log_path = os.path.join(app_path, 'logs')

if not os.path.exists(app_log_path):
    os.makedirs(app_log_path)

log_file_name = __appname__ + '.txt'

formatter = '%(asctime)s: %(name)s -%(levelname)s -%(module)s -%(funcName)s -%(lineno)-3d -%(message)s'
logging.basicConfig(filename=os.path.join(app_log_path, log_file_name),
        format=formatter)
logger = logging.getLogger(name='main-gui')
logger.setLevel(logging.DEBUG)

qtcreator_file = "mainwindow.ui"
# Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

# class Main(QMainWindow, Ui_MainWindow):
class Main(QMainWindow):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        # QMainWindow.__init__(self)
        # Ui_MainWindow.__init__(self)
        # self.setupUi(self)
        uic.loadUi('mainwindow.ui', self)

        self.init_ui()

        self.show()

    def init_ui(self):
        self.quit_button.clicked.connect(self.exit_app)
        self.calculate_tax_button.clicked.connect(self.calculate_tax)

    def calculate_tax(self):
        price = Decimal(self.le_price.text())
        tax = Decimal(self.sb_tax_rate.value())
        total_price = price + ((tax / 100) * price)
        total_price_str = f"The total price with tax is: $ {total_price:.2f}"
        self.label_result.setText(total_price_str)

    def exit_app(self):
        logger.debug("Exiting")
        sys.exit(0)

def main():
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
            termcolor.cprint("Sorry, something's wrong! ",
                             "yellow", file=sys.stderr)
            # print traceback
            traceback.print_exception(etype, value, tb)

    # Set global exception handler.
    sys.excepthook = excepthook

    # Open the app
    app = QApplication(sys.argv)
    App = Main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
