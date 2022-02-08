import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QMainWindow, QLabel, QPushButton


class ConverterWindow(QMainWindow):
    def __init__(self):
        super(ConverterWindow, self).__init__()
        self.setWindowTitle('Карта')
        uic.loadUi('main.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = ConverterWindow()
    wnd.show()
    sys.exit(app.exec())
