from PyQt5 import QtCore
import serial

class SensorReader(QtCore.QObject):
    # Signal to emit depth and temperature as two separate floats
    new_sensor_data = QtCore.pyqtSignal(float, float)

    def __init__(self, port, baudrate):
        super().__init__()
        self.serial = serial.Serial(port, baudrate)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_sensor)
        self.timer.start(1000)  # Read data every 1 second

    def read_sensor(self):
        if self.serial.in_waiting:
            data = self.serial.readline().decode('utf-8').strip()
            try:
                if data.startswith("$SDDBT"):
                    data = data.split(',')
                    depth = float(data[3])
                    print(f"Depth: {depth}")

                    # Extracting temperature and remove any checksum or extra characters
                    temperature_str = data[7].split('*')[0]
                    temperature = float(temperature_str)
                    print(f"Temperature: {temperature}")

                    # Send depth and temperature as separate values
                    self.new_sensor_data.emit(depth, temperature)
                else:
                    print(f"Received: {data}")
            except ValueError as ve:
                print(ve)
            except Exception as e:
                print(e)
