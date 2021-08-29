# pyqt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton


class BaseButton(QPushButton):
    """Recipient Base Button"""
    # sizes
    WIDTH = 90
    HEIGHT = 30
    # paddings
    PADDING_TOP = 3
    PADDING_BOTTOM = 3
    PADDING_LEFT = 0
    PADDING_RIGHT = 0
    # icon
    ICON = ''
    ICON_SIZE = 16
    # alignment
    TEXT_ALIGN = 'center'
    # chars
    CHARS = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupButton()

    def setupButton(self):
        # set icon
        if self.ICON:
            self.setIcon(QIcon(self.ICON))
            self.setIconSize(QSize(self.ICON_SIZE, self.ICON_SIZE))
        # set style
        styleSheet = f"""
            width:          {self.WIDTH}px;
            height:         {self.HEIGHT}px;
            text-align:     {self.TEXT_ALIGN};
            padding-left:   {self.PADDING_LEFT}px;
            padding-right:  {self.PADDING_RIGHT}px;
            padding-top:    {self.PADDING_TOP}px;
            padding-bottom: {self.PADDING_BOTTOM}px;
        """
        self.setStyleSheet(styleSheet)
        # adjust width
        self.adjustWidth()

    def adjustWidth(self):
        diff = len(self.text()) - self.CHARS
        if diff > 0:
            self.setFixedWidth(self.WIDTH + diff * 5)


class SMButton(BaseButton):
    """Recipeint Small Button"""
    WIDTH = 60
    HEIGHT = 20
    CHARS = 5


class MDButton(BaseButton):
    """Recipient Medium Button"""
    WIDTH = 90
    HEIGHT = 30
    CHARS = 10


class LGButton(BaseButton):
    """Recipeint Large Button"""
    WIDTH = 120
    HEIGHT = 40
    CHARS = 15


class MainMenuButton(BaseButton):
    """Recipient Main-Menu Button"""
    WIDTH = 200
    HEIGHT = 50
    TEXT_ALIGN = 'left'
    PADDING_LEFT = 20
    ICON_SIZE = 24
    CHARS = 20


class AddSMButton(SMButton):
    """Recipient Add Small Button"""
    ICON = ':icons/btnAdd.png'


class AddMDButton(MDButton):
    """Recipient Add Medium Button"""
    ICON = AddSMButton.ICON


class EditSMButton(SMButton):
    """Recipient Edit Small Button"""
    ICON = ':icons/btnEdit.png'


class EditMDButton(MDButton):
    """Recipient Edit Medium Button"""
    ICON = EditSMButton.ICON


class DeleteSMButton(SMButton):
    """Recipient Delete Small Button"""
    ICON = ':icons/btnDelete.png'


class DeleteMDButton(MDButton):
    """Recipient Delete Medium Button"""
    ICON = DeleteSMButton.ICON


class SyncSMButton(SMButton):
    """Recipient Sync Small Button"""
    ICON = ':icons/btnSync.png'


class SyncMDButton(MDButton):
    """Recipient Sync Medium Button"""
    ICON = SyncSMButton.ICON


class SaveSMButton(SMButton):
    """Recipient Save Small Button"""
    ICON = ':icons/btnSave.png'


class SaveMDButton(MDButton):
    """Recipient Save Medium Button"""
    ICON = SaveSMButton.ICON


class SaveAllSMButton(SMButton):
    """Recipient SaveAll Small Button"""
    ICON = ':icons/btnSaveAll.png'


class SaveAllMDButton(MDButton):
    """Recipient SaveAll Medium Button"""
    ICON = SaveAllSMButton.ICON


class RefreshSMButton(SMButton):
    """Recipient Refresh Small Button"""
    ICON = ':icons/btnRefresh.png'


class RefreshMDButton(MDButton):
    """Recipient Refresh Medium Button"""
    ICON = RefreshSMButton.ICON


class ClearSMButton(SMButton):
    """Recipient Clean Small Button"""
    ICON = ':icons/btnClear.png'


class ClearMDButton(MDButton):
    """Recipient Clean Medium Button"""
    ICON = ClearSMButton.ICON


class StartSMButton(SMButton):
    """Recipient Start Small Button"""
    ICON = ':icons/btnStart.png'


class StartMDButton(MDButton):
    """Recipient Start Medium Button"""
    ICON = StartSMButton.ICON


class StopSMButton(SMButton):
    """Recipient Stop Small Button"""
    ICON = ':icons/btnStop.png'


class StopMDButton(MDButton):
    """Recipient Stop Medium Button"""
    ICON = StopSMButton.ICON


class OKSMButton(SMButton):
    """Recipient OK Small Button"""
    ICON = ':icons/btnOK.png'


class CancelSMButton(SMButton):
    """Recipient Cancel Small Button"""
    ICON = ':icons/btnCancel.png'


class CancelMDButton(MDButton):
    """Recipient Cancel Medium Button"""
    ICON = CancelSMButton.ICON
