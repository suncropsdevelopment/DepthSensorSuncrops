import pyqtgraph as pg
from PyQt5 import QtGui
import numpy as np
from pyqtgraph.examples.PColorMeshItem import antialiasing
from scipy.interpolate import make_interp_spline


class PlotUpdater:
    def __init__(self,plot_graph):

        self.plot_graph = plot_graph
        self.time = []
        self.depth = []

        pen = pg.mkPen(color=(255,0,0))
        self.line = self.plot_graph.plot(
            self.time,
            self.depth,
            name = 'Depth Sensor',
            pen = pen
        )

        self.water_fill = pg.FillBetweenItem(
            self.line,
            pg.PlotDataItem([0], [0]),
            brush=pg.mkBrush(color= '#2B65EC')
        )

        self.plot_graph.addItem(self.water_fill)

        self.muddy_fill = pg.FillBetweenItem(
            self.line,
            pg.PlotDataItem([0],[0]),
            brush= pg.mkBrush(color='#C18136')
        )

        self.plot_graph.addItem(self.muddy_fill)

        self.amplitude = 5  # Height of the wave
        self.frequency = 0.1  # How often the wave oscillates
        self.phase = 0

        #self.plot_graph.setXRange(-20, 0)

    def update_plot(self,depth):
        new_time = self.time[-1]+1 if self.time else 0
        self.time.append(new_time)
        self.depth.append(depth)

        updated_time = np.linspace(min(self.time), max(self.time), 100)
        spl = make_interp_spline(self.time, self.depth, 3)
        updated_depth = spl(updated_time)

        # take 20 or more or less value at a time

        if len(self.time)>20:
            self.time = self.time[-20:]
            self.depth = self.depth[-20:]

        self.line.setData(updated_time,updated_depth)

        max_depth = max(self.depth) if self.depth else depth
        min_depth = min(self.depth) if self.depth else depth
        max_time = min(self.time)
        padding = 5
        max_value_y = max_depth

        self.water_fill.setCurves(
            self.line,
            pg.PlotDataItem(self.time,[0]*len(self.time))
        )
        self.muddy_fill.setCurves(
            self.line,
            pg.PlotDataItem(self.time,[max_value_y]*len(self.time))
        )

        self.plot_graph.setYRange(
            min(min_depth,0),
            max_value_y
        )

