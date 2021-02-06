import os
import sys

from io import BytesIO
from PIL import Image

import requests
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, \
    QLabel, QComboBox, QPushButton, QLineEdit

# Старотовая позиция
START_POS = 'Санкт-Петербург'

# Словарь со способами отображения карт(слоев)

LAYER = {
    'Схема местности и названия географических объектов': 'map',
    'Местность, сфотографированная со спутника': 'sat',
    'Местность, сфотографированная со спутника с пробками': 'sat,trf',
    'Схема местности и названия географических объектов с пробками': 'map,trf',
    'Местность, сфотографированная со спутника с пробками и названиями объектов': 'map,trf,skl',
    'Схема местности и названия географических объектов с пробками и названиями объектов': 'sat,trf,skl'
}
# !!!!!
# давайте сделаем вывод карты улицы (любой)
# нужно закрыть первую задачу
# !!!!!

# API и ключ
api_server = "http://geocode-maps.yandex.ru/1.x/"
map_api_server = "http://static-maps.yandex.ru/1.x/"
api_key = "40d1649f-0493-4b70-98ba-98533de7710b"


# про дезигн:
# search_line - место, куда узер вводит адресс
# search_btn - кнопка поиска
# reset_btn - сброс
# layers_box - комбо бокс с выбором слоев
# image - место для карты
# Основной класс приложения
class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi("design.ui", self)
        self.address = START_POS
        self.api_server = api_server
        self.map_api_server = map_api_server
        self.api_key = api_key
        self.delta = '0.005'
        self.show_second()

    # Обработка нажатия клавиш
    def keyPressEvent(self, event):
        pass
        # Заместо pgUp/pgDown используем +/-
        # if event.key() == QtCore.Qt.Key_PgUp:
        # pass
        # if event.key() == QtCore.Qt.Key_PgOn:
        # pass

    # для первой задачи
    def show_second(self):
        map = self.get_map()
        self.show_map(map)

    # ...
    def geocode(self):
        geocoder_params = {
            "apikey": self.api_key,
            "geocode": self.address,
            "format": "json"}
        response = requests.get(self.api_server,
                                params=geocoder_params)
        if not response:
            print('geocode error')
            sys.exit(1)
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        return toponym

    # Получение карты
    def get_map(self):
        ll = self.get_ll()
        params = {
            "ll": ll,
            "spn": ",".join([self.delta, self.delta]),
            "l": "map"}
        map = requests.get(url=self.map_api_server, params=params)
        if not map:
            print('get_map error')
            sys.exit(1)
        return map

    # Получение локации от узера
    def get_location(self):
        pass

    # я хочу кушать
    # os.path
    # Отображение карты
    def show_map(self, map):
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(map.content)
        self.image.setPixmap(self.pixmap)
        # pixmap = QPixmap()
        # pixmap.loadFromData(get_static_map(z=z, l=l, ll=self.ll,
        #                                    points=self.points))
        # self.map_img.setPixmap(pixmap)

    def get_ll(self):
        toponym = self.geocode()
        toponym_coords = toponym["Point"]["pos"]
        ll = toponym_coords.replace(' ', ',')
        return ll


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())
