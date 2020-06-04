from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QSplashScreen, QMainWindow
from PyQt5.QtCore import QTime, QTimer, Qt, QThread, pyqtSignal
from PyQt5 import uic
import sys
import time
import logging

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)


class Main(QMainWindow):
    INTERVAL = 10
    count = 0
    thread_counter = 0
    count1 = 0
    finished = pyqtSignal(bool)
    busy_thread = QThread()

    def __init__(self):
        super().__init__()
        uic.loadUi(r"main.ui", self)
        self.message = "Alert!"
        self.initUi()

    def initUi(self):
        # this will never work because you shouldn't move the main gui to a thread
        self.moveToThread(self.busy_thread)
        self.finished.connect(self.busy_thread.quit)
        self.busy_thread.started.connect(self.print_thread_msg)
        self.busy_thread.finished.connect(self.busy_thread.start)
        self.busy_thread.start()
        self.loop()
        self.loop3()
        self.show()

    # Timer without single shot
    def loop(self):
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.print_msg)
        self.timer.start(self.INTERVAL)

    def loop2(self):
        logger.debug("loop2")
        QTimer.singleShot(self.INTERVAL, self.finished.emit)
        # self.finished.emit()
        # time.sleep(1)
        # self.finished.emit()
        # self.busy_thread.start()
        # while True:
        #     time.sleep(1)
        #     self.finished.emit()

    # Timer with single shot
    def loop3(self):
        self.count1 %= 15
        self.count1 += 1
        self.print3LineEdit.setText(f"print3 counter: {self.count1}")
        QTimer.singleShot(self.INTERVAL, self.loop3)

    def stop(self):
        self.timer.stop()

    def print_msg(self):
        # logger.debug('printing msg')
        if self.count > 100:
            self.count = 0
        else:
            self.count += 1
        self.printLineEdit.setText(f"hello: {self.count}")

        return "reg done"

    def print_thread_msg(self):
        # logger.debug('printing from thread')
        loop = 1000
        for x in range(loop):

            if self.thread_counter > loop:
                self.thread_counter = 0
            else:
                time.sleep(1)
                self.thread_counter += 1

        self.threadLineEdit.setText(f"thread counter: {self.thread_counter}")
        self.finished.emit(True)
        # return "thread msg done"


def main():
    # Enable logging on the console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    # Opens the app
    app = QApplication(sys.argv)
    App = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
