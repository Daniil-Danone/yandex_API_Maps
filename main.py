import sys
import requests
from PyQt5 import uic
from PIL.ImageQt import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class ConverterWindow(QMainWindow):
    def __init__(self):
        print('OK')
        super(ConverterWindow, self).__init__()
        self.setWindowTitle('Карта')
        uic.loadUi('main.ui', self)
        self.image_maps()

    def image_maps(self):
        map_request = f'https://static-maps.yandex.ru/1.x/?ll=73.368221,54.989347' \
                      f'&spn=0.05,0.05&size=650,450&l=map&scale=1'
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")

        else:
            image = QImage.fromData(response.content)
            pixmap = QPixmap.fromImage(image)
            self.map.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = ConverterWindow()
    wnd.show()
    sys.exit(app.exec())
