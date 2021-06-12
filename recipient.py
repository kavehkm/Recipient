# standard
import sys
# internal
from src.ui import Main as MainWindow
from src import Controller
# pyqt
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    controller = Controller(ui)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
