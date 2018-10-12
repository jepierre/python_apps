# -*- coding: utf-8 -*-
""""
Author: Jean Pierre
Last Edited: 05/19/2018

"""

__appname__ = 'PyMonthlyExpense'
__module__ = 'main'
#__path__ = r'.\PyMonthlyExpense'
import PyMonthlyExpense.ui_files


import logging
import sys
import os
import re
from PyQt5 import (uic)
from PyQt5.QtWidgets import (QApplication, QLabel, QSplashScreen, QMainWindow, QTableWidgetItem,
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import (QTime, QTimer, Qt, QThread, pyqtSignal, QSettings, QCoreApplication)

import pandas as pd
from datetime import datetime

PATH = os.path.dirname(__file__)
print(PATH)
app_data_path = PATH
logging.basicConfig(filename=app_data_path + r'\pymonthlyexpense.log',
                    format='%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)\
                    -6d -%(message)s')
logger = logging.getLogger(name='main-gui')
logger.setLevel(logging.DEBUG)


class Main(QMainWindow):
    open_file_name = None
    save_file_name = None
    months = ['Jun 17', 'July 17', 'Aug 17', 'Sep 17', 'Oct 17', 'Nov 17', 'Dec 17', 'Jan 18', 'Feb 18', 'Mar 18',
              'Apr 18', 'May 18']


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
        self.btn_calculatetotal.clicked.connect(self.calculate_total)
        self.action_exit.triggered.connect(self.exit_app)
        self.create_table()

    def open_file(self):
        self.open_file_name = QFileDialog.getOpenFileName(self, "Open CSV File", app_data_path, 'All files (*.*)')[0]
        logger.debug(f'open_file_name: {self.open_file_name}')

    def save_file(self):
        self.save_file_name = QFileDialog.getSaveFileName(self, "Save Result", app_data_path, "All files (*.*)")[0]
        logger.debug(f'save_file_name: {self.save_file_name}')

    def calculate_total(self):
        if ((self.open_file_name is None) or not(self.open_file_name.endswith('.csv'))):
            logger.debug('Not a valid csv file')
            QMessageBox.warning(self, 'Warning', 'Not a valid csv file!')
            return False

        df = pd.read_csv(self.open_file_name, index_col='Date')
        logger.debug(f'dataframe dtypes: {df.dtypes}')
        logger.debug('remove unnecessary data columns')
        df = df.drop(columns=['Labels', 'Notes', 'Original Description'], axis=1)

        logger.debug('Removing transfer and credit transactions')
        def mask(df, key, value):
            return df[df[key] != value]
        pd.DataFrame.mask = mask
        df = df.mask('Category', 'Transfer').mask('Transaction Type', 'credit')
        df = df.loc[df['Account Name'] == 'CREDIT CARD']
        logger.debug(f'df:\n{df}')
        df.index = pd.to_datetime(df.index)

        jun_17 = df.loc['2017-6-1':'2017-6-30']
        jul_17 = df.loc['2017-7-1':'2017-7-31']
        aug_17 = df.loc['2017-8-1':'2017-8-31']
        sep_17 = df.loc['2017-9-1':'2017-9-30']
        oct_17 = df.loc['2017-10-1':'2017-10-31']
        nov_17 = df.loc['2017-11-1':'2017-11-30']
        dec_17 = df.loc['2017-12-1':'2017-12-31']
        jan_18 = df.loc['2018-1-1':'2018-1-31']
        feb_18 = df.loc['2018-2-1':'2018-2-28']
        mar_18 = df.loc['2018-3-1':'2018-3-31']
        apr_18 = df.loc['2018-4-1':'2018-4-30']
        may_18 = df.loc['2018-5-1':'2018-5-31']

        df_months = [jun_17,
                     jul_17,
                     aug_17,
                     sep_17,
                     oct_17,
                     nov_17,
                     dec_17,
                     jan_18,
                     feb_18,
                     mar_18,
                     apr_18,
                     may_18]

        df_month_sums = []
        idx = 0
        for month in df_months:
            frame = month.groupby(['Category'])['Amount'].sum().to_frame().rename(index=str,
                                                                                  columns={'Amount': self.months[idx]})
            df_month_sums.append(frame)
            idx += 1

        self.result = pd.concat(df_month_sums, join='inner', axis=1)
        logger.debug(f'result:\n{self.result}')

        self.update_table()



        # for inx, column in enumerate(result.columns):
        #     for iny, index in enumerate(result.index):
        #         logger.debug(f'{result[column][index]}')

    def create_table(self):
        # self.main_table.setRowCount(1)
        self.main_table.setColumnCount(len(self.months))
        self.main_table.setHorizontalHeaderLabels((self.months))
        # self.main_table.insertRow(0)
        # self.main_table.setHorizontalHeaderLabels('Category')
        # self.main_table.setItem(0, 0, QTableWidgetItem('Category'))
        # for index, month in enumerate(self.months):
        #     logger.debug(f'index: {index}\tmonth: {month}')
        #     self.main_table.setItem(index+1, index+1, QTableWidgetItem(month))

    def update_table(self):
        logger.debug('updating table')
        self.main_table.setRowCount(len(self.result.index))
        self.main_table.setVerticalHeaderLabels(self.result.index)

        for inx, column in enumerate(self.result.columns):
            for iny, index in enumerate(self.result.index):
                logger.debug(f'{self.result[column][index]}')
                self.main_table.setItem(iny, inx, QTableWidgetItem(f'{self.result[column][index]:{12}.{5}}'))


    def exit_app(self):
        sys.exit(0)



def main():
    # __path__ = os.path.dirname(__file__)
    # sys.path.insert(0, __path__)
    os.chdir(os.path.dirname(__file__))
    # __path__ = os.getcwd()
    # print(f'path: {__path__}')
    # print(f'sys: {sys.path}')
    QCoreApplication.setApplicationName('PyMonthlyExpense')
    QCoreApplication.setApplicationVersion('0.1')
    QCoreApplication.setOrganizationName('PyMonthlyExpense')
    QCoreApplication.setOrganizationDomain('pymonthlyexpense.com')

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