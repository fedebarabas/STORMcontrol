#!/usr/bin/env python3

from __future__ import with_statement

import time

#from numpy import arange, sin, pi
import numpy as np

# QT IMPORTS
from PyQt4.uic import loadUi
from PyQt4.QtCore import QThread, QObject, SIGNAL, SLOT
from PyQt4.QtGui import QWidget, QMainWindow, qApp

from matplotlib import pyplot as plt

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
        delta = random.uniform(-0.5, 0.5)
        r = random.random()

        if r > 0.9:
            self.data += delta * 15
        elif r > 0.8:
            # attraction to the initial value
            delta += (0.5 if self.init > self.data else -0.5)
            self.data += delta
        else:
            self.data += delta

class Connections(QMainWindow):

    def __init__(self, laser1, laser2, zstage, daq, *args, **kwargs):

        super().__init__(*args, **kwargs)

        loadUi('STORMgui.ui', self)

        QObject.connect(self.actionQuit, SIGNAL('triggered()'), qApp,
        SLOT("quit()"))

        QObject.connect(self.pushButton, SIGNAL("clicked()"), self.update_graph)

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

        instruments = [laser1, laser2, zstage, daq]

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
            connect_driver(self, stagez, prefix='stagez')

            ### MOVE Z STAGE TO ITS DYNAMIC RANGE CENTER AND DEFINE IT AS Z = 0
            stagez.move_absolute(50 * um)
            stagez.position = 0 * um

        focus_lock_on = self.findChild((QWidget, ), 'focus_lock_on')
        focus_lock_on.clicked.connect(handletoggle)

        # connect the signals with the slots
        #open_push = self.findChild((QWidget, ), 'mplpushButton')
        #open_push

#        plot_on = self.findChild((QWidget, ), 'pushButton')
#        plot_on.clicked.connect(self.update_graph)

        def update_graph(self):
            x = np.arange(0, 10, 0.2)
            y = np.sin(x)
            self.mpl.canvas.ax.plot(x, y)
            self.mpl.canvas.fig.draw()





