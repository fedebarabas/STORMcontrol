#!/usr/bin/env python3

import sys
import argparse

# LANTZ IMPORTS
#import lantz.ui
#from lantz import Q_
#
from PyQt4.QtGui import QApplication

app = QApplication(sys.argv)

from STORMconnections import Connections, DynamicPlotter, amplitude

# UNIT DEFINITIONS
#mW = Q_(1, 'milliwatt')
#um = Q_(1, 'micrometer')

# COMMAND-LINE ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument('-p640', '--port640', type=str, default='COM3',
                    help='COM port for the 640nm laser')
parser.add_argument('-p405', '--port405', type=str, default='COM4',
                    help='COM port for the 405nm laser')
parser.add_argument('-pz', '--portz', type=str, default='COM1',
                    help=
                    ('COM port for the Z stage or the ProScanII controller'
                    'if the NanoScanZ is connected to it through its '
                    'RS232-2 port'))
parser.add_argument('-pu12', '--portu12', type=int, default=0,
                    help='Port for the LabJack U12 interface')
parser.add_argument('-t', '--test',
                    help=
                    ('Run without connecting instruments, just for interface '
                    'testing'), action='store_true')

args = parser.parse_args()

# TEST MODE
if args.test:

    main = Connections(None, None, None, None)
    
    main.show()
    
    m = DynamicPlotter(main.ui.lockplot, amplitude, sampleinterval=0.05, 
                           timewindow=10.)
                           
    exit(app.exec_())

# MAIN MODE
else:

    # DRIVER IMPORTS
    from lantz.drivers.rgblasersystems import MiniLasEvo
    from lantz.drivers.prior import NanoScanZ_chained
    from lantz.drivers.labjack import U12

    with MiniLasEvo(args.port640) as laser640, \
         MiniLasEvo(args.port405) as laser405, \
         NanoScanZ_chained(args.portz) as stagez, \
         U12(args.portu12) as u12:

        ### CHECKING THE ACCESS TO ALL INSTRUMENTS
        print((laser640.idn))
        print((laser405.idn))
        print((stagez.idn))
        print((u12.idn))

        # print(u12.analog_in[1])

        main = Connections(laser640, laser405, stagez, u12)

        main.show()
        
        m = DynamicPlotter(main.ui.lockplot, amplitude, sampleinterval=0.05, 
                           timewindow=10.)        
        
        exit(app.exec_())