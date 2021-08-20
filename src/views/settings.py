# internal
from src import settings as s
from src.ui.components import Message


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
            'general': s.get('general'),
            'wc': s.get('wc'),
            'moein': s.get('moein'),
            'invoices': s.get('invoices')
        })
        self.ui.contents.showTab(self.ui.contents.SETTINGS)

    def save(self):
        try:
            settings = self.tab.get()
            s.set('general', settings['general'])
            s.set('wc', settings['wc'])
            s.set('moein', settings['moein'])
            s.set('invoices', settings['invoices'])
            s.save()
        except Exception as e:
            lvl = Message.ERROR
            msg_txt = 'Cannot Save Settings'
            details = str(e)
        else:
            lvl = Message.SUCCESS
            msg_txt = 'Settings Saved Successfully.'
            details = None
        msg = Message(self.ui, lvl, msg_txt, details)
        msg.show()

    def clear(self):
        self.tab.clear()
