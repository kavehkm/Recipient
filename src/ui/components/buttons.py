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
    ICON_SIZE = 32
    # alignment
    TEXT_ALIGN = 'center'

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


class SMButton(BaseButton):
    """Recipeint Small Button"""
    WIDTH = 60
    HEIGHT = 20
    ICON_SIZE = 24


class MDButton(BaseButton):
    """Recipient Medium Button"""
    WIDTH = 90
    HEIGHT = 30
    ICON_SIZE = 32


class LGButton(BaseButton):
    """Recipeint Large Button"""
    WIDTH = 120
    HEIGHT = 40
    ICON_SIZE = 48


class MainMenuButton(BaseButton):
    """Recipient Main-Menu Button"""
    WIDTH = 200
    HEIGHT = 50
    TEXT_ALIGN = 'left'
    PADDING_LEFT = 20
