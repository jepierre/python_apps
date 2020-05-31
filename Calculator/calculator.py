# -*- coding: utf-8 -*-
""""
Author: Jean Pierre
Last Edited: 05/19/2018

calculator.py
http://zetcode.com/gui/pyqt5/layout/
"""
__appname__ = "Calculator"


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


class Calculator(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

        self.setWindowTitle(__appname__)
        self.setGeometry(300, 300, 320, 240)
        # self.setStyleSheet('background-color: pink')
        self.setFixedSize(self.size())
        self.show()

    def init_ui(self):
        self.centra_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.le_output = QLineEdit("")
        self.le_result = QLineEdit()
        self.le_result.setAlignment(Qt.AlignRight)
        self.le_result.setStyleSheet("font: bold 50px;" "color: gray")
        self.le_result.setReadOnly(True)
        self.le_output.setReadOnly(True)
        self.le_output.setAlignment(Qt.AlignRight)
        self.main_layout.addWidget(self.le_result)
        self.main_layout.addWidget(self.le_output)
        self.buttons = []
        grid = QGridLayout()

        self.names = [
            "Cls",
            "Bck",
            "",
            "Close",
            "7",
            "8",
            "9",
            "/",
            "4",
            "5",
            "6",
            "*",
            "1",
            "2",
            "3",
            "-",
            "0",
            ".",
            "=",
            "+",
        ]

        positions = [(i, j) for i in range(5) for j in range(4)]

        for position, name in zip(positions, self.names):
            if name == "":
                continue
            button = QPushButton(name)
            self.buttons.append(button)

            grid.addWidget(button, *position)
        self.main_layout.addLayout(grid)
        self.main_layout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        self.setLayout(self.main_layout)
        self.centra_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.centra_widget)

        for button in self.buttons:
            # logger.debug(f'button: {button.text()}')
            button.clicked.connect(lambda x, button=button: self.update_ui(button))

    def update_ui(self, button):
        button_name = button.text()
        logger.debug(f"button: {button_name}")

        if button_name in self.names[4:] and button_name != "=":
            self.le_output.setText(self.le_output.text() + button.text())

        elif button_name == "Close":
            sys.exit()

        elif button_name == "Cls":
            self.le_output.clear()
            self.le_result.clear()

        elif button_name == "Bck":
            # removes last character in output
            self.le_output.setText(self.le_output.text()[:-1])

        elif button_name == "=":
            try:
                result = eval(self.le_output.text())
                self.le_result.setText(str(result))
            except Exception as error:
                self.le_result.setText("Error!")
                logger.debug(f"Error: {error}")


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
    calculator = Calculator()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
