# standard
import sys
# internal
from src.ui import UI
# pyqt
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
