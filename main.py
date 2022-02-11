import os
import sys
import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt
from dotenv import load_dotenv
from PIL.ImageQt import QImage
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow


path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(path):
    load_dotenv(path)

    API_ID = os.environ.get('API_COMPANYS')


class MapWindow(QMainWindow):
    def __init__(self):
        super(MapWindow, self).__init__()
        uic.loadUi('main.ui', self)

#  инициализация окна

        self.setWindowIcon(QIcon('media/google_maps_128px.png'))
        self.setWindowTitle(f'Многофункциональная карта Земли [650x450] ®Danone & Авокато')
        self.setFixedSize(650, 450)

#  функции кнопок и оформление
        self.layers_icon.setPixmap(QPixmap('media/layers.png'))
        self.layers_butt.clicked.connect(self.layers_change)

        self.search_butt.setIcon(QIcon('media/search_20px.png'))
        self.search_butt.clicked.connect(self.search)
        self.search_field.returnPressed.connect(self.search_butt.click)

        self.clear_butt.setIcon(QIcon('media/delete_20px.png'))
        self.clear_butt.clicked.connect(self.clear)

        self.menu_butt.setIcon(QIcon('media/menu_32px.png'))
        self.menu_butt.clicked.connect(self.menu_show)

#  переменные

        self.layer = 'map'
        self.spn = 0.01
        self.x = 73.368221
        self.y = 54.989347
        self.mark = False

        self.map.setFocus(True)

        self.image_maps()

    def image_maps(self):
        if self.mark is True:
            map_request = f'https://static-maps.yandex.ru/1.x/?pt={self.x},{self.y},pm2rdm&size=650,450&l={self.layer}' \
                          f'&spn={self.spn},{self.spn}'
        else:
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

    def search(self):
        if self.search_field.text() is not None:
            response_text = self.search_field.text()
            request = f'https://search-maps.yandex.ru/v1/?apikey={API_ID}&text={response_text}&lang=ru_RU&format=json'
            response = requests.get(request)
            if response:
                data = response.json()

                coordinates = data['features'][0]['geometry']['coordinates']
                self.spn = 0.0025
                self.x = coordinates[0]
                self.y = coordinates[1]
                self.mark = True
                self.image_maps()
                response.close()

            else:
                print("Ошибка выполнения запроса:")
                print('fff')
                print(response)
                print("Http статус:", response.status_code, "(", response.reason, ")")

    def clear(self):
        self.search_field.clear()

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
        if self.menuBox.x() == -250:
            self.menuBox.move(10, 40)
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
