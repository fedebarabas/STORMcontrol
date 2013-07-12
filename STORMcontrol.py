if __name__ == '__main__':

	import argparse
	import time
	from lantz import Q_
	from lantz.drivers.rgblasersystems import MiniLasEvo

	parser = argparse.ArgumentParser()
   	# Configure
	parser.add_argument('-p', '--port', type=str, default='COM3', help='COM port')
	args = parser.parse_args()
	
	mW = Q_(1, 'milliwatt')
	
	with MiniLasEvo(args.port) as laser640:
		laser640.initialize()
		laser640.enabled = True
		print(laser640.idn)
		laser640.power = 1 * mW
		time.sleep(6)
		laser640.enabled = False
		laser640.finalize()