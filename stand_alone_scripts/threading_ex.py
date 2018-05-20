from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QSplashScreen, QMainWindow
from PyQt5.QtCore import QTime, QTimer, Qt, QThread, pyqtSignal
from PyQt5 import uic

import time
import logging
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

import sys

class Main(QMainWindow):
    INTERVAL = 100
    count = 0
    thread_counter = 0
    finished = pyqtSignal()

    def __init__(self, parent=None):
        self.message = 'Alert!'
        super().__init__(parent)
        uic.loadUi(r'main.ui', self)
        self.busy_thread = QThread()
        self.actionExit.triggered.connect(sys.exit)
        self.initUi()

    def initUi(self):
        self.loop()
        self.moveToThread(self.busy_thread)
        self.finished.connect(self.busy_thread.quit)
        # self.finished.connect(self.print_thread_msg)
        self.busy_thread.started.connect(self.loop2)
        # self.busy_thread.finished.connect(self.busy_thread.deleteLater)
        self.busy_thread.finished.connect(self.print_thread_msg)
        self.busy_thread.start()
        self.show()

    def loop(self):
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.print_msg)
        self.timer.start(self.INTERVAL)

    def loop2(self):
        logger.debug('loop2')
        QTimer.singleShot(self.INTERVAL, self.finished.emit)
        # self.finished.emit()
        # time.sleep(1)
        # self.finished.emit()
        # self.busy_thread.start()
        # while True:
        #     time.sleep(1)
        #     self.finished.emit()

    def stop(self):
        self.timer.stop()

    def print_msg(self):
        logger.debug('printing msg')
        if self.count > 100:
            self.count = 0
        else:
            self.count += 1
        self.le_msg.setText(f'hello: {self.count}')

    def print_thread_msg(self):
        logger.debug('printing from thread')
        if self.thread_counter > 1000:
            self.thread_counter = 0
        else:
            self.thread_counter += 1

        self.le_thread_msg.setText(f'thread counter: {self.thread_counter}')
        self.busy_thread.start()

def main():
    # Enable logging on the console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # Opens the app
    app = QApplication(sys.argv)
    App = Main()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()