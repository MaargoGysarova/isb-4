import hashlib
import multiprocessing as mp
import sys
import time

from PyQt6.QtCore import QBasicTimer, Qt
from PyQt6.QtWidgets import (QApplication, QFormLayout, QLabel, QMainWindow,
                             QProgressBar, QPushButton, QSlider, QVBoxLayout,
                             QWidget)

from hash import algorithm_luna, check_hash
from settings import SETTING

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Hash function collision search')
        self.resize(600, 600)
        self.setStyleSheet('background-color: #dbdcff;')
        self.info_card = QLabel(
            f'Available card information: {SETTING["begin_digits"]}******{SETTING["last_digits"]}')
        layout = QVBoxLayout()
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.pbar.hide()
        self.timer = QBasicTimer()
        self.timer.stop()
        title_slider = QLabel('Select number of pools:', self)
        self.result_label = QLabel('Result:')
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
        self.start_button.clicked.connect(self.find_solution)
        layout.addWidget(self.start_button)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        def search_card_number(self, start_time: float):
            """функция поиска номера карты
            Args:
                start (float): время начала поиска
            """
            with mp.Pool(self.value) as p:
                for i, result in enumerate(p.map(check_hash, range(99999, 10000000))):
                    if result:
                        self.update_pb_on_success(start_time, result)
                        p.terminate()
                        break
                    self.update_pb_on_progress(i)
                else:
                    self.result_label.setText('Solution not found')
                    self.pbar.setValue(100)