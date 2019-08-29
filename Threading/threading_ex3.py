"""
based on the tutorial:
https://nikolak.com/pyqt-threading-tutorial/
"""
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QSplashScreen, QMainWindow
from PyQt5.QtCore import QTime, QTimer, Qt, QThread, pyqtSignal, QObject, QRunnable, QThreadPool
from PyQt5 import uic
import sys
import time
import logging
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)


# Note that a QRunnable isn't a subclass of QObject and therefore does
# not provide signals and slots.
# this keeps running even after app quits
class RunableThread(QRunnable):
    finished = pyqtSignal()

    def __init__(self, line_edit):
        super(RunableThread, self).__init__()
        self.threadLineEdit = line_edit

    def run(self):
        logger.debug('printing from thread 3')
        loop = 1000

        for x in range(loop):
            logger.debug(f"thread 3: in loop: {x}")
            time.sleep(1)

            self.threadLineEdit.setText(f'thread counter: {x}')
        self.finished.emit()


class WorkerThread(QThread):
    threadLineEdit = None
    thread_counter = 0

    def __init__(self, line_edit):
        super(WorkerThread, self).__init__()
        self.threadLineEdit = line_edit

    def run(self):
        logger.debug('printing from thread 1')
        loop = 1000
        for x in range(loop):
            logger.debug(f"in loop: {x}")

            if self.thread_counter > loop:
                self.thread_counter = 0
            else:
                time.sleep(1)
                self.thread_counter += 1

            self.threadLineEdit.setText(f'thread counter: {self.thread_counter}')


class ObjectToThread(QObject):
    finished = pyqtSignal()

    def __init__(self, line_edit):
        super(ObjectToThread, self).__init__()
        self.thread2LineEdit = line_edit

    def long_running_process(self):
        logger.debug('printing from thread 2')
        loop = 1000

        for x in range(loop):
            logger.debug(f"thread 2: in loop: {x}")
            time.sleep(1)

            self.thread2LineEdit.setText(f'thread counter: {x}')
        self.finished.emit()


class Main(QMainWindow):

    class TempClass(QThread):
        def __init__(self):
            QThread.__init__(self)

        def run(self):
            for x in range(1000):
                logger.debug(f'in temp class: {x}')
                time.sleep(1)


    tmp_clas = TempClass()
    INTERVAL = 1000
    count = 0
    thread_counter = 0
    count1 = 0
    finished = pyqtSignal(bool)
    my_thread = QThread()

    def __init__(self):
        super().__init__()
        uic.loadUi(r'main.ui', self)
        self.init_ui()

    def init_ui(self):
        self.temp_thread = self.TempClass()
        self.temp_thread.finished.connect(self.print_all_done)
        self.temp_thread.start()
        self.print_msg()
        self.use_qthread()
        self.use_runnable()
        self.use_move_to_thread()
        self.show()

    def use_runnable(self):
        myrunnable = RunableThread(self.thread3LineEdit)

        QThreadPool.globalInstance().start(myrunnable)

    def use_qthread(self):
        self.message_thread = WorkerThread(self.threadLineEdit)
        self.message_thread.finished.connect(self.print_all_done)
        self.message_thread.start()

    def use_move_to_thread(self):
        # in order for this to work:
        # 1. you can't put main application window in a thread
        # 2. my thread has to be defined globally
        self.obj = ObjectToThread(self.thread2LineEdit)
        self.obj.moveToThread(self.my_thread)
        self.obj.finished.connect(self.my_thread.quit)
        self.my_thread.started.connect(self.obj.long_running_process)
        self.my_thread.finished.connect(self.print_all_done)
        self.my_thread.start()

    def print_all_done(self):
        logger.debug("all done")


    # Timer with single shot
    def print_msg(self):
        self.count1 %= 1000
        self.count1 += 1
        self.printLineEdit.setText(f'print counter: {self.count1}')
        QTimer.singleShot(self.INTERVAL, self.print_msg)


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

if __name__ == '__main__':
    main()