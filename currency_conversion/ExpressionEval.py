# -*- coding: utf-8 -*-
"""
Author: Jean Pierre
Last Edited:
https://www.udemy.com/python-gui-programming/learn/v4/overview

"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.results_list = QTextBrowser()
        self.results_input = QLineEdit('Enter an expression and press return key.')

        layout = QVBoxLayout()
        layout.addWidget(self.results_list)
        layout.addWidget(self.results_input)
        self.setLayout(layout)

        self.results_input.selectAll()
        self.results_input.setFocus()

        self.results_input.returnPressed.connect(self.compute)
        self.setWindowTitle('Expression Evaluations')

        self.show()

    def compute(self):
        try:
            text = self.results_input.text()
            self.results_list.append(f'{text} = <b>{eval(text)}</b>')
        except:
            self.results_list.append("<font color=red><b>Expression invalid</b></font>")

def main():
    app = QApplication(sys.argv)
    App = Form()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
