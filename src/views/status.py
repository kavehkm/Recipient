# standard
from threading import Event
# internal
from src import settings as s
from src.wc import ConnectionsError
from src.ui.components import Message
from src.worker import NetworkChecker
# pyqt
from PyQt5.QtCore import QThread, QObject, pyqtSignal, QThreadPool


class RecipientEngineSignals(QObject):
    """Recipient Engine Signals"""
    error = pyqtSignal(object)


class RecipientEngine(QThread):
    """Recipient Engine"""
    def __init__(self, interval, wc_update, convert_orders):
        super().__init__()
        self._interval = interval
        self.wc_update = wc_update
        self.convert_orders = convert_orders
        # events
        # - stop
        self.stop_event = Event()
        # - resume
        self.resume_event = Event()
        # signals
        self.signals = RecipientEngineSignals()

    def start(self):
        # set resume event
        self.resume_event.set()
        # clear stop event
        self.stop_event.clear()
        super().start()

    def pause(self):
        self.resume_event.clear()

    def resume(self):
        self.resume_event.set()

    def stop(self):
        # set stop event
        self.stop_event.set()
        self.quit()
        # set resume event
        self.resume_event.set()

    def _do(self):
        # check for orders
        if self.convert_orders:
            print('convert orders')
        # check for wc models update
        if self.wc_update:
            print('wc update')

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
        # get settings
        settings = s.get('engine')
        # recipient engine
        self.engine = RecipientEngine(
            settings['interval'],
            settings['wc_update'],
            settings['convert_orders']
        )
        # ui
        self.ui = ui
        self.tab = ui.contents.status
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
        if isinstance(error, ConnectionsError):
            # put tab state on connecting...
            self.tab.connecting()
            # create network checker
            nc = NetworkChecker(s.IP, s.PORT, s.TIMEOUT, s.INTERVAL, s.JITTER)
            # connect signals
            nc.signals.connected.connect(self.nc_connected_handler)
            nc.signals.tik.connect(self.tab.connecting_count)
            # move to thread pool and start
            QThreadPool.globalInstance().start(nc)
        else:
            self.engine.stop()
            msg = Message(self.ui, Message.ERROR, 'Engine stop working.', str(error))
            msg.show()

    def nc_connected_handler(self):
        # put tab state on start
        self.tab.start()
        # resume engine
        self.engine.resume()
