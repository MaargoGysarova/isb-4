import multiprocessing as mp
import sys, time
import numpy as np
from PyQt6.QtCore import QBasicTimer, Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import (QApplication, QFormLayout, QLabel, QMainWindow,
                             QProgressBar, QPushButton, QSlider, QVBoxLayout,
                             QWidget, QComboBox)
from hash import algorithm_luna, check_hash
from settings import SETTING


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.result_curd = None
        self.setWindowTitle('SEARCH OF BANK CARD')
        self.setFixedSize(600, 400)
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 600, 400)
        self.background.setPixmap(QPixmap("wallpaper_isb-4.png").scaled(600, 400))
        btn_StyleSheet_main = 'background-color: #ffffff; color: #4682B4; border :1px solid;'

        self.info_card = QLabel(
            f'Available card information: {SETTING["begin_digits"]}******{SETTING["last_digits"]}')
        layout = QVBoxLayout()
        self.info_card.setStyleSheet(btn_StyleSheet_main)
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.pbar.hide()
        self.timer = QBasicTimer()
        self.timer.stop()
        title_slider = QLabel('Select number of pools:', self)
        title_slider.setStyleSheet(btn_StyleSheet_main)
        self.result_label = QLabel('Result:')
        self.result_label.setStyleSheet(btn_StyleSheet_main)
        layout = QFormLayout()
        self.setLayout(layout)
        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setRange(1, 64)
        slider.setSingleStep(1)
        slider.setValue(36)
        slider.valueChanged.connect(self.updateLabel)
        self.value_label = QLabel('', self)
        self.value = slider.value()
        layout.addRow(self.info_card)
        layout.addRow(title_slider)
        layout.addRow(slider)
        layout.addRow(self.value_label)
        layout.addRow(self.result_label)
        layout.addRow(self.pbar)
        self.start_button = QPushButton('To start searching')
        title_slider.setStyleSheet(btn_StyleSheet_main)
        self.start_button.clicked.connect(self.pb_and_time)
        layout.addWidget(self.start_button)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def search_card_number(self, start_time: float):
        """функция поиска номера карты
        Args:
            start (float): время начала поиска
            :param start_time:
            :param self:
        """
        times = np.empty(shape=0)
        with mp.Pool(self.value) as p:
            for i, result in enumerate(p.map(check_hash, range(99999, 10000000))):
                if result:
                    self.update_pb_on_finish(start_time, result)
                    p.terminate()
                    break
                self.update_pb_on_progress(i)
            else:
                self.result_label.setText('Solution not found')
                self.pbar.setValue(100)


    def pb_and_time(self):
        """Функция подгатавливает прогресс бар, задает время начала и вызывает функцию поиска номера карты
        """
        self.prepare_pb()
        start = time.time()
        self.search_card_number(start)

    def prepare_pb(self):
        """Подготавливает прогресс бар и выводит начальную информацию
        """
        self.result_label.setText('Search in progress...')
        self.pbar.show()
        if not self.timer.isActive():
            self.timer.start(100, self)
        QApplication.processEvents()

    def update_pb_on_finish(self, start_time: float, result: float):
        """Обновляет прогресс бар и выводит информацию о карте и времени поиска
        Args:
        start (float): время начала
        result (float): время окончания поиска
        """
        self.result_curd = result
        self.pbar.setValue(100)
        end = time.time() - start_time
        result_text = f'Found number of card: {result}\n'
        result_text += f'Checking the Luhn Algorithm: {algorithm_luna(result)}\n'
        result_text += f'Time of process: {end:.2f} seconds'
        self.info_card.setText(
            f'Available card information: {SETTING["begin_digits"]}{result}{SETTING["last_digits"]}')
        self.result_label.setText(result_text)

    def update_pb_on_progress(self, i: int):
        """Обновляет ползунок pb
        Args:
        i (int): значение итерации
        """
        self.pbar.setValue(int((i + 1) / len(range(99999, 10000000)) * 100))

    def updateLabel(self, value: int):
        """Функция, которая обновляет значение числа в слайдере
        Args:
        value (int): число ядер
        """
        self.value_label.setText(str(value))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
