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
