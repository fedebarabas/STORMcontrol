import sys
import argparse

import lantz.ui
from lantz import Q_
from lantz.ui.qtwidgets import connect_driver
from Qt.QtGui import QApplication, QWidget
from Qt.uic import loadUi

from lantz.drivers.rgblasersystems import MiniLasEvo

app = QApplication(sys.argv)
main = loadUi('STORM_gui.ui')

mW = Q_(1, 'milliwatt')

parser = argparse.ArgumentParser()
parser.add_argument('-p640', '--port640', type=str, default='COM3', help='COM port for the 640nm laser')
parser.add_argument('-p405', '--port405', type=str, default='COM4', help='COM port for the 405nm laser')
args = parser.parse_args()

with MiniLasEvo(args.port640) as laser640, \
     MiniLasEvo(args.port405) as laser405:
	print(laser640.idn)
	print(laser640.operating_hours, 'operating hours')
	print(laser405.idn)
	print(laser405.operating_hours, 'operating hours')
	
	# enabled = main.findChild((QWidget, ), 'enabled')
	# power = main.findChild((QWidget, ), 'power')
	
	# connect_driver(main, [laser640, laser405])
	connect_driver(main, laser640, prefix='laser640')
	connect_driver(main, laser405, prefix='laser405')
	
	main.show()
	exit(app.exec_())	
