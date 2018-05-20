# -*- coding: utf-8 -*-
"""
Author:
Last Edited:
https://www.udemy.com/python-gui-programming/learn/v4/overview
"""
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import urllib.request
import json

import logging
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
logger.addHandler(ch)
from decimal import Decimal

class Form(QDialog):
    country_code = open('Common-Currency.json', encoding='cp65001').read()
    # logger.debug(country_code)
    country_code_json_list = json.loads(country_code)
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        date = self.get_data()
        rates = sorted(self.rates.keys())

        date_label = QLabel(date)

        self.fromComboBox = QComboBox()
        self.toComboBox = QComboBox()

        self.fromComboBox.addItems(rates)
        self.toComboBox.addItems(rates)

        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 1000)
        self.fromSpinBox.setValue(1.00)

        self.toLabel = QLabel('1.00')

        layout = QGridLayout()
        layout.addWidget(date_label, 0, 0)
        layout.addWidget(self.fromComboBox, 1, 0)
        layout.addWidget(self.toComboBox, 2, 0)
        layout.addWidget(self.fromSpinBox, 1, 1)
        layout.addWidget(self.toLabel, 2, 1)
        self.setLayout(layout)

        self.fromComboBox.currentIndexChanged.connect(self.update_ui)
        self.toComboBox.currentIndexChanged.connect(self.update_ui)
        self.fromSpinBox.valueChanged.connect(self.update_ui)

        self.show()

    def get_data(self):
        self.rates = {}

        try:
            date = '05/13/2018'
            # fh = urllib.request.urlopen('https://openexchangerates.org/api/latest.json?app_id=3406849eef8a4155864710586c0f6f59&base=USD').read()
            fh = open('latest.json').read()

            data = json.loads(fh, parse_float=Decimal)
            for rate in data['rates']:
                value = float(data['rates'][rate])
                if rate in self.country_code_json_list:
                    self.rates[self.country_code_json_list[rate]['name_plural']] = value

            return "Exchage rates date: " + date
        except Exception as e:
            return f"Failure to download:\n{e}"

    def get_country_name(self, iso_3_name):
        for country_code in self.country_code_json_list:
            logger.debug(f'country: {country_code["alpha3"]}, iso_name: {iso_3_name}')
            if country_code['alpha3'] == iso_3_name:
                return country_code['name']





    def update_ui(self):
        from_ = self.fromComboBox.currentText()
        to_ = self.toComboBox.currentText()

        results = (self.rates[to_] / self.rates[from_]) * self.fromSpinBox.value()
        self.toLabel.setText('%0.3f' % results)



def main():
    app = QApplication(sys.argv)
    App = Form()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()