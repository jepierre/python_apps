# https://stackoverflow.com/questions/32141623/pyqt5-and-asyncio-yield-from-never-finishes
# https://pypi.org/project/Quamash/

import sys
import asyncio
import time
import logging

from PyQt5 import uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QProgressBar, QMainWindow
from quamash import QEventLoop, QThreadExecutor

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)

sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(0)


sys.excepthook = exception_hook


class WorkerThread(QThread):
    def __init__(self, func):
        QThread.__init__(self)
        self.func = func

    def run(self):
        self.func()


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi(r"main.ui", self)
        self.async_task = None
        self.worker_thread = None
        self.worker_thread2 = None
        self.init_ui()

    def init_ui(self):
        self.start_pb.clicked.connect(self.master)
        self.start_pb.clicked.connect(self.write_hello)

    def print_thread3(self):
        for x in range(1000):
            logger.debug(f"in temp class: {x}")
            self.thread3LineEdit.setText(f"in temp class: {x}")
            time.sleep(0.01)

    # def print_thread2(self):
    #     for x in range(10000):
    #         logger.debug(f'in thread 2: {x}')
    #         self.thread2LineEdit.setText(f"Thread 2: {x}")
    #         time.sleep(.1)

    # @asyncio.coroutine
    # def master(self):
    #     with loop:
    #         yield self.run_progress_bar()
    # loop.run_until_complete(self.run_progress_bar())
    # yield self.run_progress_bar()
    # with loop:
    #     loop.run_until_complete(self.run_progress_bar())
    # with QThreadExecutor(1) as exec:
    #     yield from loop.run_in_executor(exec, self.last_50)

    def master(self):
        if self.async_task is None:
            self.async_task = asyncio.ensure_future(self.run_progress_bar(), loop=loop)
        elif not self.async_task.cancelled():
            self.async_task.cancel()
            self.async_task = None

        # if self.worker_thread is None:
        #     self.worker_thread = WorkerThread(self.print_thread3)
        #     self.worker_thread.finished.connect(lambda: logger.debug("Done"))
        #     self.worker_thread.start()
        # elif self.worker_thread.isRunning():
        #     self.worker_thread.terminate()
        #     self.worker_thread = None

        # if self.worker_thread2 is None:
        #     self.worker_thread2 = WorkerThread(self.print_thread2)
        #     self.worker_thread2.finished.connect(lambda: logger.debug("Done"))
        #     self.worker_thread2.start()
        # elif self.worker_thread2.isRunning():
        #     self.worker_thread2.terminate()
        #     self.worker_thread2 = None

    async def run_progress_bar(self):
        logger.debug("run progress bar")
        for i in range(100):
            logger.debug(f"index: {i}")
            self.progress_bar.setValue(i)
            await asyncio.sleep(0.1)

    def write_hello(self):
        logger.debug("writing hello")
        self.printLineEdit.setText("hello")


if __name__ == "__main__":
    # Enable logging on the console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    App = Main()
    App.show()
    sys.exit(app.exec_())

    # with loop:
    #     loop.run_forever()
