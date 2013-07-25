import sys
import argparse
import time

# LANTZ IMPORTS
import lantz.ui
from lantz import Q_
from lantz.ui.qtwidgets import connect_driver
from Qt.QtGui import QApplication, QWidget
#from PySide.QtGui import *
#from PySide.QtCore import *
from Qt.uic import loadUi
from Qt.QtCore import QThread, QObject

# DRIVER IMPORTS
from lantz.drivers.rgblasersystems import MiniLasEvo
from lantz.drivers.prior import NanoScanZ_chained
from lantz.drivers.labjack import U12

app = QApplication(sys.argv)
main = loadUi('STORM_gui.ui')

# UNIT DEFINITIONS
mW = Q_(1, 'milliwatt')
um = Q_(1, 'micrometer')

# COMMAND-LINE ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument('-p640', '--port640', type=str, default='COM3', help='COM port for the 640nm laser')
parser.add_argument('-p405', '--port405', type=str, default='COM4', help='COM port for the 405nm laser')
parser.add_argument('-pz', '--portz', type=str, default='COM1', help='COM port for the Z stage or the ProScanII controller if the NanoScanZ is connected to it through its RS232-2 port')
args = parser.parse_args()

with MiniLasEvo(args.port640) as laser640, \
     MiniLasEvo(args.port405) as laser405, \
     NanoScanZ_chained(args.portz) as stagez, \
     U12(0) as u12:

    ### CHECKING THE ACCESS TO ALL INSTRUMENTS
    print(laser640.idn)
    print(laser405.idn)
    print(stagez.idn)
    print(u12.idn)

    print(u12.analog_in[1])

    
    ### MAXIMUM POWER BUTTONS
    def set_powermax(inst):
        inst.power = inst.maximum_power
    laser640__powermax = main.findChild((QWidget, ), 'laser640__powermax')
    laser640__powermax.clicked.connect(lambda: set_powermax(laser640))
    laser405__powermax = main.findChild((QWidget, ), 'laser405__powermax')
    laser405__powermax.clicked.connect(lambda: set_powermax(laser405))
    ###
   
    ### CONNECTING DRIVERS TO WIDGETS
    connect_driver(main, laser640, prefix='laser640')
    connect_driver(main, laser405, prefix='laser405')
    connect_driver(main, stagez, prefix='stagez')
    focus_lock_on = main.findChild((QWidget, ), 'focus_lock_on')
    
    ### MOVE Z STAGE TO ITS DYNAMIC RANGE CENTER AND DEFINE IT AS Z = 0
    stagez.move_absolute(50 * um)
    stagez.position = 0 * um
    
    ### FOCUS LOCK FUNCTION
    class Focus_lock(QThread):
        def __init__(self, parent = None):
            QThread.__init__(self, parent)
            self.exiting = False

        def run(self):
            while self.exiting==False:
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
            
                
    focus_lock_on.clicked.connect(handletoggle)
    ###


    main.show()
    exit(app.exec_())   
