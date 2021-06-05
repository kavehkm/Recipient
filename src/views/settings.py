# internal
from src import settings as s
from src.ui.widgets import Message


class Settings(object):
    """Settings View"""
    def __init__(self, ui):
        self.ui = ui
        self.tab = ui.contents.settings
        # connect signals
        self.ui.menu.btnSettings.clicked.connect(self.tab_handler)
        self.tab.btnSave.clicked.connect(self.save)
        self.tab.btnClear.clicked.connect(self.clear)

    def tab_handler(self):
        self.tab.set({
            'wc': s.get('wc', {}),
            'moein': s.get('moein', {})
        })
        self.ui.contents.showTab(self.ui.contents.SETTINGS)

    def save(self):
        try:
            settings = self.tab.get()
            s.set('wc', settings.get('wc'))
            s.set('moein', settings.get('moein'))
            s.save()
        except Exception as e:
            lvl = Message.ERROR
            msg_txt = 'Cannot Save Settings'
            details = str(e)
        else:
            lvl = Message.SUCCESS
            msg_txt = 'Settings Saved Successfully.'
            details = None
        msg = Message(self.tab, lvl, msg_txt, details)
        msg.show()

    def clear(self):
        self.tab.clear()
