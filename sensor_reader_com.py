from PyQt5 import QtCore
import serial

class SensorReader(QtCore.QObject):
    new_depth_data = QtCore.pyqtSignal(float)

    def __init__(self,port,baudrate):
        super().__init__()
        self.serial = serial.Serial(port,baudrate)
        self.timer  =QtCore.QTimer()
        self.timer.timeout.connect(self.read_sensor)
        self.timer.start(500)

    def read_sensor(self):
        if self.serial.in_waiting:
            data = self.serial.readline().decode('utf-8').strip()
            try:
                depth = float(data)
                self.new_depth_data.emit(depth)
            except ValueError:
                print("Invalid Sensor Data.")