# -*- coding: utf-8 -*-
""""
Author: Jean Pierre
Last Edited: 05/19/2018

"""

__appname__ = "PyMonthlyExpense"
__module__ = "main"

import logging
import os
import sys
import termcolor
import traceback
from calendar import monthrange

import pandas as pd
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
    QFileDialog,
    QMessageBox,
)
from PyMonthlyExpense.plain_text_edit_logger import CustomLoggerWidget

PATH = os.path.dirname(__file__)
print(PATH)
app_data_path = PATH
logging.basicConfig(
    filename=app_data_path + r"\pymonthlyexpense.log",
    format="%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)\
                    -6d -%(message)s",
)
logger = logging.getLogger(name="main-gui")
logger.setLevel(logging.DEBUG)


class Main(QMainWindow):
    open_file_name = None
    save_file_name = None
    year = None
    result = None
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        uic.loadUi(r"ui_files\main.ui", self)
        logger.debug("loading main.ui")
        self.setWindowTitle(__appname__)
        self.init_ui()

        self.show()

    def init_ui(self):
        self.action_open.triggered.connect(self.open_file)
        self.action_save.triggered.connect(self.save_file)
        self.action_save_as.triggered.connect(self.save_as_file)
        self.btn_calculatetotal.clicked.connect(self.calculate_total)
        self.action_exit.triggered.connect(self.exit_app)
        self.create_table()

        # adds text docker and pins custom logger to it
        custom_logger = CustomLoggerWidget(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, custom_logger)

        # set current year to combox year
        self.cb_year.currentIndexChanged.connect(self.set_year)

        # todo: set stylesheet using qt designer
        # logger.debug('adding stylesheet')
        # # adds a stylesheet
        # # self.main_table.setStyleSheet("""
        # #     font: 12pt "Sitka Text";
        # #     background: rgb(204, 199, 255);
        # #     """)

        logger.debug("adding year to combo box")
        # todo: update combo box based on years in the transaction file
        self.cb_year.addItems(["2018", "2019", "2020"])

    def set_year(self):
        self.year = int(self.cb_year.currentText())

    def open_file(self):
        self.open_file_name = QFileDialog.getOpenFileName(
            self, "Open CSV File", app_data_path, "All files (*.*)"
        )[0]
        logger.debug(f"open_file_name: {self.open_file_name}")
        # if self.open_file_name:
        #     self.save_file_name = os.path.splitext(self.open_file_name)[0] + '_result.xlsx'

    def save_file(self):
        if not self.open_file_name:
            return
        if not self.save_file_name:
            self.save_file_name = (
                os.path.splitext(self.open_file_name)[0] + "_result.xlsx"
            )
            self.save_as_file()
            return

        logger.debug(f"save_file_name: {self.save_file_name}")
        if self.save_file_name and self.result is not None:
            self.result.to_excel(self.save_file_name)

    def save_as_file(self):
        self.save_file_name = QFileDialog.getSaveFileName(
            self, "Save Result", self.save_file_name, "Excel Files (.xlsx);;All (*.*)"
        )[0]
        logger.debug(f"save_file_name: {self.save_file_name}")
        if self.save_file_name and self.result is not None:
            self.result.to_excel(self.save_file_name)

    def calculate_total(self):
        if (self.open_file_name is None) or not (self.open_file_name.endswith(".csv")):
            logger.debug("Not a valid csv file")
            QMessageBox.warning(self, "Warning", "Not a valid csv file!")
            return False

        # let's create the table here
        self.create_table()

        df = pd.read_csv(self.open_file_name, index_col="Date")
        logger.debug(f"dataframe dtypes: {df.dtypes}")

        logger.debug("Removing unnecessary data columns")
        df = df.drop(columns=["Labels", "Notes", "Original Description"], axis=1)

        logger.debug("Removing transfer and credit transactions")

        def mask(df, key, value):
            return df[df[key] != value]

        pd.DataFrame.mask = mask
        df = df.mask("Category", "Transfer").mask("Transaction Type", "credit")
        df = df.loc[df["Account Name"] == "CREDIT CARD"]
        logger.debug(f"df:\n{df}")

        logger.debug("Changing date index to datetime values")
        df.index = pd.to_datetime(df.index)

        df_months = []
        for idx, month in enumerate(self.months):
            idx = idx + 1
            last_day = monthrange(self.year, idx)[1]  # get last day of the month
            mask = (df.index >= f"{self.year}-{idx}-1") & (
                df.index <= f"{self.year}-{idx}-{last_day}"
            )
            df_months.append(df[mask])

        df_month_sums = []
        for df_month, month in zip(df_months, self.months):
            if not df_month.empty:
                frame = (
                    df_month.groupby(["Category"])["Amount"]
                    .sum()
                    .to_frame()
                    .rename(index=str, columns={"Amount": f"{month} {self.year}"})
                )
                df_month_sums.append(frame)
        if not df_month_sums:
            logger.info("There's no matching transactions. Quitting!")
            return

        self.result = pd.concat(df_month_sums, axis=1, sort=True)
        self.result.fillna(0, inplace=True)
        logger.debug(f"result:\n{self.result}")

        # add median column
        self.result["Median"] = self.result.median(axis=1)

        # add total row to result
        self.result = self.result.append(
            self.result.sum(numeric_only=True).rename("Total")
        )

        self.update_table()

    def create_table(self):
        # clear the table first
        self.clear_table()

        self.main_table.setColumnCount(len(self.months))
        self.main_table.setHorizontalHeaderLabels(self.months)

    def clear_table(self):
        self.main_table.setRowCount(0)

    def update_table(self):
        logger.debug("updating table")
        self.main_table.setColumnCount(len(self.result.columns))
        self.main_table.setHorizontalHeaderLabels(self.result.columns)
        """ todo: use designer to create stylesheet
         stylesheet = "::section{background: red;}"
         self.main_table.horizontalHeader().setStyleSheet(stylesheet)
         """
        self.main_table.setRowCount(len(self.result.index))
        self.main_table.setVerticalHeaderLabels(self.result.index)

        for inx, column in enumerate(self.result.columns):
            for iny, index in enumerate(self.result.index):
                logger.debug(f"{self.result[column][index]}")
                self.main_table.setItem(
                    iny, inx, QTableWidgetItem(f"$ {self.result[column][index]:,.2f}")
                )

    def exit_app(self):
        sys.exit(0)


def main():
    os.chdir(os.path.dirname(__file__))
    QCoreApplication.setApplicationName("PyMonthlyExpense")
    QCoreApplication.setApplicationVersion("0.1")
    QCoreApplication.setOrganizationName("PyMonthlyExpense")
    QCoreApplication.setOrganizationDomain("pymonthlyexpense.com")

    # Enable logging on the console
    ch = logging.StreamHandler()
    ch.setFormatter(
        logging.Formatter(
            "%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)\
                    -6d -%(message)s"
        )
    )
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
    App = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
