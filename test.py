import sys
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np


class PlotUpdater:
    def __init__(self, plot_graph):
        self.plot_graph = plot_graph
        self.time = [0]  # Initialize with a starting value
        self.depth = [0]  # Initialize with a starting value

        # Customize the x-axis to show only whole numbers
        self.plot_graph.setLabel('bottom', 'Time')
        self.plot_graph.getAxis('bottom').setTickSpacing(major=1, minor=0)  # Set major ticks to 1 unit

        # Plot the initial line
        pen = pg.mkPen(color=(255, 0, 0))
        self.line = self.plot_graph.plot(
            self.time,
            self.depth,
            name='Depth Sensor',
            pen=pen
        )

        # Add water fill
        self.water_fill = pg.FillBetweenItem(
            self.line,
            pg.PlotDataItem([0], [0]),
            brush=pg.mkBrush(color='#2B65EC')
        )
        self.plot_graph.addItem(self.water_fill)

        # Add muddy fill
        self.muddy_fill = pg.FillBetweenItem(
            self.line,
            pg.PlotDataItem([0], [0]),
            brush=pg.mkBrush(color='#C18136')
        )
        self.plot_graph.addItem(self.muddy_fill)

        # Add vehicle fill
        self.vehicle_fill = pg.FillBetweenItem(
            self.line,
            pg.PlotDataItem([0], [0]),
            brush=pg.mkBrush(color='#52d8f8')
        )
        self.plot_graph.addItem(self.vehicle_fill)

        # Add a fixed line
        self.distance = 50
        self.fixed_line = pg.InfiniteLine(
            pos=-self.distance,
            angle=0,
            pen=pg.mkPen(color='white', width=2, style=QtCore.Qt.DashLine)
        )
        self.plot_graph.addItem(self.fixed_line)

        # Add a zero line
        self.zero_line = pg.InfiniteLine(
            pos=0,
            angle=0,
            pen=pg.mkPen(color='d', width=2, style=QtCore.Qt.DashLine)
        )
        self.plot_graph.addItem(self.zero_line)

        # Add a text label
        self.text_label = pg.TextItem(anchor=(1, 1), color='#000000')
        self.text_label.setFont(QtGui.QFont('Arial', 10))
        self.plot_graph.addItem(self.text_label)

        # Set initial plot range
        self.plot_graph.setXRange(0, 20, padding=0)
        self.plot_graph.setYRange(-self.distance, 0, padding=0)

    def update_plot(self, depth):
        # Append new data
        new_time = self.time[-1] + 1 if self.time else 0
        self.time.append(new_time)
        self.depth.append(depth)

        # Keep only the last 20 data points
        if len(self.time) > 20:
            self.time = self.time[-20:]
            self.depth = self.depth[-20:]

        # Update the line data
        self.line.setData(self.time, self.depth)

        # Update the fill areas
        max_depth = max(self.depth) if self.depth else depth
        min_depth = min(self.depth) if self.depth else depth
        padding = 5

        self.water_fill.setCurves(
            self.line,
            pg.PlotDataItem(self.time, [0] * len(self.time))
        )
        self.muddy_fill.setCurves(
            self.line,
            pg.PlotDataItem(self.time, [max_depth] * len(self.time))
        )
        self.vehicle_fill.setCurves(
            pg.PlotDataItem(self.time, [-self.distance] * len(self.time)),
            pg.PlotDataItem(self.time, [0] * len(self.time))
        )

        # Update the plot range
        self.plot_graph.setYRange(
            min(min_depth, -self.distance),
            max(max_depth, 0),
            padding=padding
        )
        self.plot_graph.setXRange(self.time[0], self.time[-1], padding=padding)

        # Update the text label
        text_x_pos = self.time[-1]
        text_y_pos = -self.distance / 2
        self.text_label.setPos(text_x_pos, text_y_pos)
        self.text_label.setText(f"Depth: {self.depth[-1]}")

        print(f"Label Position: x={text_x_pos}, y={text_y_pos}")


# Example usage
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    win.setWindowTitle('PyQtGraph Plot Updater Example')
    win.resize(800, 600)

    # Create a PlotWidget
    plot_widget = pg.PlotWidget()
    win.setCentralWidget(plot_widget)

    # Initialize the PlotUpdater
    plot_updater = PlotUpdater(plot_widget)

    # Simulate data updates
    def simulate_data():
        import random
        depth = random.uniform(-50, 50)
        plot_updater.update_plot(depth)
        QtCore.QTimer.singleShot(500, simulate_data)  # Update every 500ms

    simulate_data()

    win.show()
    sys.exit(app.exec_())