import sys
import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PIL.ImageQt import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class ConverterWindow(QMainWindow):
    def __init__(self):
        super(ConverterWindow, self).__init__()

        self.setWindowTitle('Карта')
        uic.loadUi('main.ui', self)
        self.setFixedSize(650, 450)

        self.spn = 0.01
        self.x = 73.368221
        self.y = 54.989347

        self.map.setFocus(True)

        self.image_maps()

    def image_maps(self):
        map_request = f'https://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}' \
                      f'&spn={self.spn},{self.spn}&size=650,450&l=map'
        response = requests.get(map_request)
        print(self.spn)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")

        else:
            image = QImage.fromData(response.content)
            pixmap = QPixmap.fromImage(image)
            self.map.setPixmap(pixmap)
            response.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.spn > 0.0001:
                self.spn = self.spn / 2
                self.image_maps()

        elif event.key() == Qt.Key_PageDown:
            if self.spn < 90:
                self.spn = self.spn * 2
                self.image_maps()

        elif event.key() == Qt.Key_Left:
            if self.x < 180.0 or self.x > -180.0:
                self.x -= 0.01
                self.image_maps()

        elif event.key() == Qt.Key_Right:
            if self.x < 180.0 or self.x > -180.0:
                self.x += 0.01
                self.image_maps()

        elif event.key() == Qt.Key_Up:
            if self.y < 90.0 or self.x > -90.0:
                self.y += 0.01
                self.image_maps()

        elif event.key() == Qt.Key_Down:
            if self.y < 90.0 or self.x > -90.0:
                self.y -= 0.01
                self.image_maps()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = ConverterWindow()
    wnd.show()
    sys.exit(app.exec())
