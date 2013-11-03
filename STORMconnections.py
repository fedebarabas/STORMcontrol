#!/usr/bin/env python3

from __future__ import with_statement

import time
import numpy as np
import math
import random
import collections

from PyQt4.uic import loadUi
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

from lantz.ui.qtwidgets import connect_driver
from lantz import Q_
from pint import UnitRegistry

ureg = UnitRegistry()
um = Q_(1, 'micrometer')

def amplitude():
    frequency = 0.5
    noise = random.normalvariate(0., 1.)
    new = 10.*math.sin(time.time()*frequency*2*math.pi) + noise
    return new * ureg.volt

class DynamicPlotter():

    def __init__(self, widget, func, sampleinterval=0.1, timewindow=10.):
        # Data stuff
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=np.float)
        
        self.func = func
      
        self.plt = widget
        
        pg.setConfigOptions(antialias=True)
#        self.plt = pg.plot(title='Dynamic Plotting with PyQtGraph')
        size = [widget.width(), widget.height()]
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', self.func.__name__, self.func().units)
        self.plt.setLabel('bottom', 'time', 's')
        self.curve = self.plt.plot(self.x, self.y, pen='y')
        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)
        
    def updateplot(self):
        self.databuffer.append( self.func().magnitude )
        self.y[:] = self.databuffer
        self.curve.setData(self.x, self.y)

class Connections(QtGui.QMainWindow):

    def __init__(self, laser640, laser405, zstage, daq, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.ui = loadUi('STORMgui.ui', self)
        self.ui.actionQuit.triggered.connect(QtGui.qApp.quit)
       

        ### FOCUS LOCK FUNCTION
        class Focus_lock(QtCore.QThread):
            def __init__(self, parent=None):
                QtCore.QThread.__init__(self, parent)
                self.exiting = False

            def run(self):
                while self.exiting == False:
                    time.sleep(1)
                    print('looping')

        thread = Focus_lock()

        def handletoggle(self):
            if thread.isRunning():
                thread.exiting = True
                while thread.isRunning():
                    time.sleep(0.01)
                    continue
            else:
                thread.exiting = False
                thread.start()
                while not thread.isRunning():
                    time.sleep(0.01)
                    continue

        self.ui.focus_lock_on.clicked.connect(handletoggle)

        instruments = [laser640, laser405, zstage, daq]

        if not None in instruments:

            ### MAXIMUM POWER BUTTONS
            def set_powermax(inst):
                inst.power = inst.maximum_power
            laser640__powermax = self.findChild((QtGui.QWidget, ),
            'laser640__powermax')
            laser640__powermax.clicked.connect(lambda: set_powermax(laser640))
            laser405__powermax = self.findChild((QtGui.QWidget, ),
            'laser405__powermax')
            laser405__powermax.clicked.connect(lambda: set_powermax(laser405))

            ### CONNECTING DRIVERS TO WIDGETS
            connect_driver(self, laser640, prefix='laser640')
            connect_driver(self, laser405, prefix='laser405')
            connect_driver(self, zstage, prefix='stagez')

            ### MOVE Z STAGE TO ITS DYNAMIC RANGE CENTER AND DEFINE IT AS Z = 0
            zstage.move_absolute(50 * um)
            zstage.position = 0 * um
        