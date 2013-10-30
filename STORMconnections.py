#!/usr/bin/env python3

from __future__ import with_statement

import time

#from numpy import arange, sin, pi
import numpy as np

# QT IMPORTS
from PyQt4.uic import loadUi
from PyQt4.QtCore import QThread, QObject, QTimer, SIGNAL, SLOT
from PyQt4.QtGui import QWidget, QMainWindow, qApp, QApplication

import pyqtgraph as pg

#from lantz.ui.qtwidgets import connect_driver
#from lantz import Q_
#
#um = Q_(1, 'micrometer')

class DataGen(object):
    """ A silly class that generates pseudo-random data for
        display in the plot.
    """
    def __init__(self, init=50):
        self.data = self.init = init

    def next(self):
        self._recalc_data()
        return self.data

    def _recalc_data(self):
        delta = np.random.uniform(-0.5, 0.5)
        r = np.random.random()

        if r > 0.9:
            self.data += delta * 15
        elif r > 0.8:
            # attraction to the initial value
            delta += (0.5 if self.init > self.data else -0.5)
            self.data += delta
        else:
            self.data += delta

class Connections(QMainWindow):

    def __init__(self, laser640, laser405, zstage, daq, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.ui = loadUi('STORMgui.ui', self)
        self.ui.show()

        QObject.connect(self.actionQuit, SIGNAL('triggered()'), qApp,
        SLOT("quit()"))

        #QObject.connect(self.pushButton, SIGNAL("clicked()"), self.update_graph)

        ### FOCUS LOCK FUNCTION
        class Focus_lock(QThread):
            def __init__(self, parent=None):
                QThread.__init__(self, parent)
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

        instruments = [laser640, laser405, zstage, daq]

        if not None in instruments:

            ### MAXIMUM POWER BUTTONS
            def set_powermax(inst):
                inst.power = inst.maximum_power
            laser640__powermax = self.findChild((QWidget, ),
            'laser640__powermax')
            laser640__powermax.clicked.connect(lambda: set_powermax(laser640))
            laser405__powermax = self.findChild((QWidget, ),
            'laser405__powermax')
            laser405__powermax.clicked.connect(lambda: set_powermax(laser405))

            ### CONNECTING DRIVERS TO WIDGETS
            connect_driver(self, laser640, prefix='laser640')
            connect_driver(self, laser405, prefix='laser405')
            connect_driver(self, zstage, prefix='stagez')

            ### MOVE Z STAGE TO ITS DYNAMIC RANGE CENTER AND DEFINE IT AS Z = 0
            zstage.move_absolute(50 * um)
            zstage.position = 0 * um

        focus_lock_on = self.findChild((QWidget, ), 'focus_lock_on')
        focus_lock_on.clicked.connect(handletoggle)

        #timer = QTimer(self)
        #QObject.connect(timer, SIGNAL("timeout()"), self.ui.mpl.canvas.update_figure)
        #timer.start(1000)

        lockplot = self.ui.lockplot
        lockplot.setLabel('left', 'Value', units='V')
        lockplot.setLabel('bottom', 'Time', units='s')
        pg.setConfigOptions(antialias=True)
        curve = lockplot.plot(pen='y')
        data = np.random.normal(size=(10,1000))
        ptr = 0
        def update():
            global curve, data, ptr, p6
            curve.setData(data[ptr%10])
            if ptr == 0:
                lockplot.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
            ptr += 1
        timer = QTimer()
        timer.timeout.connect(update)
        timer.start(50)
