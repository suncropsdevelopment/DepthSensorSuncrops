from random import randint
from PyQt5 import QtCore


class SensorReader(QtCore.QObject):
    new_depth_data = QtCore.pyqtSignal(float,float)  # Signal for both depth and temperature

    def __init__(self):
        super().__init__()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_sensor)
        self.timer.start(1000)

    def read_sensor(self):
        # Generate random depth between 5 and 200
        depth = randint(5, 200)

        # Generate random temperature between -10 and 40
        temperature = randint(-10, 40)

        # Emit both depth and temperature as a tuple
        self.new_depth_data.emit(depth,temperature)