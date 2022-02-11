import sys
import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PIL.ImageQt import QImage
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow


class MapWindow(QMainWindow):
    def __init__(self):
        super(MapWindow, self).__init__()

        self.setWindowTitle('Карта')
        uic.loadUi('main.ui', self)
        self.setFixedSize(650, 450)

        self.layers_icon.setPixmap(QPixmap('media/layers_38px.png'))
        self.menu_icon.setPixmap(QPixmap('media/menu_32px.png'))

        self.layers_butt.clicked.connect(self.layers_change)
        self.menu_butt.clicked.connect(self.menu_show)
        self.search_field.clearFocus()

        self.layer = 'map'
        self.spn = 0.01
        self.x = 73.368221
        self.y = 54.989347
        self.menu_x = self.menuBox.x()

        self.image_maps()

    def image_maps(self):
        map_request = f'https://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}' \
                      f'&spn={self.spn},{self.spn}&size=650,450&l={self.layer}'
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

    def layers_change(self):
        if self.layer == 'map':
            self.layer = 'sat'
        elif self.layer == 'sat':
            self.layer = 'sat,skl'
        else:
            self.layer = 'map'
        self.image_maps()
        self.map.setFocus(True)

    def menu_show(self):
        self.menu_x = self.menuBox.x()
        if self.menu_x == -250:
            self.menuBox.move(10, 50)
        else:
            self.menuBox.move(-250, 50)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.spn > 0.0001:
                self.spn = self.spn / 2
                self.image_maps()

        elif event.key() == Qt.Key_PageDown:
            if self.spn < 40:
                self.spn = self.spn * 2
            self.image_maps()

        elif event.key() == Qt.Key_Left:
            self.map.setFocus(True)
            if self.x < 180.0 or self.x > -180.0:
                self.x -= 0.01 * self.spn * 100
                if self.x < -180:
                    self.x = 180 - abs(self.x + 180)
                    print(self.x)
                self.image_maps()

        elif event.key() == Qt.Key_Right:
            self.map.setFocus(True)
            if self.x < 180.0 or self.x > -180.0:
                self.x += 0.01 * self.spn * 100
                if self.x > 180:
                    self.x = -180 + abs(self.x - 180)
                self.image_maps()

        elif event.key() == Qt.Key_Up:
            self.map.setFocus(True)
            if self.y < 90.0:
                self.y += 0.01 * self.spn * 100
                if self.y > 90:
                    self.y = 90
            self.image_maps()

        elif event.key() == Qt.Key_Down:
            self.map.setFocus(True)
            if self.x > -90.0:
                self.y -= 0.01 * self.spn * 100
                if self.y < -90:
                    self.y = -90
            self.image_maps()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MapWindow()
    wnd.show()
    sys.exit(app.exec())
