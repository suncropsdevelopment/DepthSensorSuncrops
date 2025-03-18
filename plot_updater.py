import pyqtgraph as pg
from PyQt5 import QtGui,QtCore
import numpy as np
from pyqtgraph.examples.PColorMeshItem import antialiasing


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

        self.vehicle_fill  =pg.FillBetweenItem(
            self.line,
            pg.PlotDataItem([0],[0]),
            brush = pg.mkBrush(color='#52d8f8')
        )

        self.plot_graph.addItem(self.vehicle_fill)


        #Adding a fixed line

        self.distance = 50
        self.fixed_line = pg.InfiniteLine(
            pos = -self.distance,
            angle=0,
            pen= pg.mkPen(color='white',width = 2, style = QtCore.Qt.DashLine)
        )

        self.plot_graph.addItem(self.fixed_line)

        self.zero_line = pg.InfiniteLine(
            pos = 0,
            angle= 0,
            pen = pg.mkPen(color='d',width=2,style=QtCore.Qt.DashLine)

        )

        self.plot_graph.addItem(self.zero_line)


        #self.plot_graph.setXRange(-20, 0)

    def update_plot(self,depth,temp):
        new_time = self.time[-1]+1 if self.time else 0
        self.time.append(new_time)
        self.depth.append(depth)

        print(temp)


        # take 20 or more or less value at a time

        if len(self.time)>20:
            self.time = self.time[-20:]
            self.depth = self.depth[-20:]

        self.line.setData(self.time,self.depth)

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

        self.vehicle_fill.setCurves(
            pg.PlotDataItem(self.time, [-self.distance] * len(self.time)),
            pg.PlotDataItem(self.time,[0]*len(self.time))
        )

        self.plot_graph.setYRange(
            min(min_depth,-self.distance),
            max(max_value_y,0),
            padding=0
        )

