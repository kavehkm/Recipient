# standard
import time
import random
from threading import Event
# pyqt
from PyQt5.QtCore import QThread


class RecipientEngine(QThread):
    """Recipient Engine"""
    def __init__(self, interval):
        super().__init__()
        self._interval = interval
        # stop event
        self.stop_event = Event()

    def stop(self):
        # set stop event
        self.stop_event.set()
        self.quit()

    def start(self):
        # clear stop event
        self.stop_event.clear()
        super().start()

    def _do(self):
        time.sleep(2)
        print(random.randint(1, 1000))

    def run(self):
        # do-while(stop_event is not set)
        while True:
            try:
                self._do()
            except Exception as e:
                pass
            else:
                if self.stop_event.wait(self._interval):
                    break


class Status(object):
    """Status View"""
    def __init__(self, ui):
        # ui
        self.ui = ui
        self.tab = ui.contents.status

        # recipient engine
        self.engine = RecipientEngine(10)

        # connect signals
        # - ui
        self.ui.menu.btnStatus.clicked.connect(self.tab_handler)
        self.tab.btnStart.clicked.connect(self.start)
        self.tab.btnStop.clicked.connect(self.stop)
        # - engine
        self.engine.started.connect(self.tab.start)
        self.engine.finished.connect(self.tab.stop)

    def tab_handler(self):
        self.ui.contents.showTab(self.ui.contents.STATUS)

    def start(self):
        self.engine.start()

    def stop(self):
        self.engine.stop()
