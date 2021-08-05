# standard
import time
import random
from threading import Event
# internal
from src.ui.components import Message
# pyqt
from PyQt5.QtCore import QThread, QObject, pyqtSignal


class RecipientEngineSignals(QObject):
    """Recipient Engine Signals"""
    error = pyqtSignal(object)


class RecipientEngine(QThread):
    """Recipient Engine"""
    def __init__(self, interval):
        super().__init__()
        self._interval = interval
        # events
        # - stop
        self.stop_event = Event()
        # - resume
        self.resume_event = Event()
        self.resume_event.set()
        # signals
        self.signals = RecipientEngineSignals()

    def start(self):
        # clear stop event
        self.stop_event.clear()
        super().start()

    def pause(self):
        self.resume_event.clear()

    def resume(self):
        self.resume_event.set()

    def stop(self):
        # set resume event
        self.resume_event.set()
        # set stop event
        self.stop_event.set()
        self.quit()

    def _do(self):
        time.sleep(2)
        random_int = random.randint(1, 1000)
        print(random_int)
        if random_int > 700:
            raise Exception('some many tears')

    def run(self):
        # do-while(stop_event is not set)
        while True:
            try:
                self._do()
            except Exception as e:
                self.pause()
                self.signals.error.emit(e)
                # check for pause event
            self.resume_event.wait()
            # check for stop event
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
        self.engine.signals.error.connect(self.engine_error_handle)

    def tab_handler(self):
        self.ui.contents.showTab(self.ui.contents.STATUS)

    def start(self):
        self.engine.start()

    def stop(self):
        self.engine.stop()

    def engine_error_handle(self, error):
        msg = Message(self.ui, Message.ERROR, 'Error', str(error))
        msg.show()
        self.engine.stop()
