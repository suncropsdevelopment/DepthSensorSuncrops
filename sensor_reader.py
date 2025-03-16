from random import randint
from PyQt5 import QtCore

class SensorReader(QtCore.QObject):
    new_depth_data = QtCore.pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.timer  =QtCore.QTimer()
        self.timer.timeout.connect(self.read_sensor)
        self.timer.start(500)

    def read_sensor(self):
        depth = randint(5,200)
        self.new_depth_data.emit(depth)