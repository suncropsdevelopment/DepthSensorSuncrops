import sys
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
from sensor_reader_com import SensorReader
from plot_updater import PlotUpdater
import serial.tools.list_ports  # For listing available COM ports

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # Create a central widget and set the layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        top_layout = QtWidgets.QVBoxLayout()
        self.com_port_dropdown = QtWidgets.QComboBox()
        self.populate_com_ports()
        self.com_port_dropdown.setFixedWidth(150)
        top_layout.addWidget(self.com_port_dropdown)

        self.baud_rate_dropdown = QtWidgets.QComboBox()
        self.baud_rate_dropdown.addItems(["9600", "19200", "38400", "57600", "115200"])
        self.baud_rate_dropdown.setFixedWidth(150)
        top_layout.addWidget(self.baud_rate_dropdown)

        # Add the top layout to the main layout
        layout.addLayout(top_layout)

        # Create the plot widget
        self.plot_graph = pg.PlotWidget()
        layout.addWidget(self.plot_graph)

        # Configure the plot widget
        self.plot_graph.setBackground('black')
        self.plot_graph.setTitle("Depth vs Time", color='grey', size="20px")
        style = {'color': 'white', 'font-size': '18px'}
        self.plot_graph.setLabel('right', 'Depth(m)', **style)
        self.plot_graph.setLabel('bottom', 'Time(sec)', **style)
        self.plot_graph.showAxis('right')
        self.plot_graph.hideAxis('left')
        self.plot_graph.invertY()
        self.plot_graph.addLegend()

        # Initialize the plot updater
        self.plot_updater = PlotUpdater(self.plot_graph, self)

        # Initialize the sensor reader (will be updated when COM port/baud rate is selected)
        self.sensor_reader = None

        # Connect dropdown changes to update the sensor reader
        self.com_port_dropdown.currentTextChanged.connect(self.update_sensor_reader)
        self.baud_rate_dropdown.currentTextChanged.connect(self.update_sensor_reader)

        # Initialize the sensor reader with the default values
        self.update_sensor_reader()


    def populate_com_ports(self):
        self.com_port_dropdown.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.com_port_dropdown.addItem(port.device)
        if not ports:
            self.com_port_dropdown.addItem("No COM ports found")

    def update_sensor_reader(self):
        com_port = self.com_port_dropdown.currentText()
        baud_rate = int(self.baud_rate_dropdown.currentText())

        if com_port != "No COM ports found":
            self.sensor_reader = SensorReader(com_port, baud_rate)
            self.sensor_reader.new_sensor_data.connect(self.plot_updater.update_plot)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())