import pyqtgraph as pg
from PyQt5 import QtGui, QtCore
import numpy as np
from scipy.interpolate import make_interp_spline  # For B-spline interpolation


class PlotUpdater:
    def __init__(self, plot_graph):
        self.plot_graph = plot_graph
        self.time = []
        self.depth = []

        # Pen for the original data line
        pen = pg.mkPen(color=(255, 0, 0))
        self.line = self.plot_graph.plot(
            self.time,
            self.depth,
            name='Depth Sensor',
            pen=pen
        )

        # Pen for the B-spline interpolated line
        self.spline_pen = pg.mkPen(color=(0, 255, 0), width=2)
        self.spline_line = self.plot_graph.plot([], [], pen=self.spline_pen, name='B-spline Interpolation')

        # Water fill
        self.water_fill = pg.FillBetweenItem(
            self.line,
            pg.PlotDataItem([0], [0]),
            brush=pg.mkBrush(color='#2B65EC')
        )
        self.plot_graph.addItem(self.water_fill)

        # Muddy fill
        self.muddy_fill = pg.FillBetweenItem(
            self.line,
            pg.PlotDataItem([0], [0]),
            brush=pg.mkBrush(color='#C18136')
        )
        self.plot_graph.addItem(self.muddy_fill)

        # Fixed line
        self.distance = 5
        self.fixed_line = pg.InfiniteLine(
            pos=-self.distance,
            angle=0,
            pen=pg.mkPen(color='white', width=2, style=QtCore.Qt.DashLine)
        )
        self.plot_graph.addItem(self.fixed_line)

        # Wave parameters
        self.amplitude = 5  # Height of the wave
        self.frequency = 0.1  # How often the wave oscillates
        self.phase = 0

    def update_plot(self, depth):
        new_time = self.time[-1] + 1 if self.time else 0
        self.time.append(new_time)
        self.depth.append(depth)

        # Keep only the last 20 data points
        if len(self.time) > 20:
            self.time = self.time[-20:]
            self.depth = self.depth[-20:]

        # Update the original data line
        self.line.setData(self.time, self.depth)

        # Perform B-spline interpolation
        if len(self.time) >= 4:  # Need at least 4 points for a cubic B-spline
            # Create a B-spline interpolation
            spline = make_interp_spline(self.time, self.depth, k=3)  # Cubic B-spline
            # Generate finer time points for smooth curve
            time_fine = np.linspace(min(self.time), max(self.time), num=100)
            depth_fine = spline(time_fine)
            # Update the B-spline line
            self.spline_line.setData(time_fine, depth_fine)
        else:
            # If not enough points, clear the B-spline line
            self.spline_line.setData([], [])

        # Update fills
        max_depth = max(self.depth) if self.depth else depth
        min_depth = min(self.depth) if self.depth else depth
        max_value_y = max_depth

        self.water_fill.setCurves(
            self.line,
            pg.PlotDataItem(self.time, [0] * len(self.time))
        )
        self.muddy_fill.setCurves(
            self.line,
            pg.PlotDataItem(self.time, [max_value_y] * len(self.time))
        )

        # Set Y-axis range without padding
        self.plot_graph.setYRange(
            min(min_depth, -self.distance),
            max(max_value_y, 0),
            padding=0  # Remove padding
        )