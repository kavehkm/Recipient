# standard
import time
import socket
# pyqt
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal


class WorkerSignals(QObject):
    """Worker Signals"""
    progress = pyqtSignal(int)
    error = pyqtSignal(object)
    result = pyqtSignal(object)
    done = pyqtSignal()


class Worker(QRunnable):
    """Worker"""
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self._fn = fn
        self._args = args
        self._kwargs = kwargs
        # attach signals
        self.signals = WorkerSignals()
        # pass progress signal to fn
        self._kwargs['progress_callback'] = self.signals.progress

    def run(self):
        try:
            result = self._fn(*self._args, **self._kwargs)
        except Exception as e:
            self.signals.error.emit(e)
        else:
            self.signals.done.emit()
            self.signals.result.emit(result)


class NetworkCheckerSignals(QObject):
    """NetworkChecker Signals"""
    tik = pyqtSignal(int)
    connected = pyqtSignal()


class NetworkChecker(QRunnable):
    """Network Checker"""
    def __init__(self, ip, port, timeout, interval, jitter):
        super().__init__()
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.interval = interval
        self.jitter = jitter
        # signals
        self.signals = NetworkCheckerSignals()

    def atempt(self):
        try:
            s = socket.create_connection((self.ip, self.port), self.timeout)
        except OSError:
            return False
        else:
            s.close()
            return True

    def run(self):
        while True:
            if self.atempt():
                self.signals.connected.emit()
                return
            else:
                for counter in range(self.interval, 0, -1):
                    time.sleep(1)
                    self.signals.tik.emit(counter)
                self.interval += self.jitter
