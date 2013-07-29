from Qt.uic import loadUiType
from Qt.QtCore import QThread, QObject

Form_class, qt_class = loadUiType('STORMgui.ui')

class Connections(Form_class):

    def __init__(self, laser1, laser2, zstage, daq, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
       
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
    

        instruments = [laser1, laser2, zstage, daq]

        if not None in instruments:

            ### MAXIMUM POWER BUTTONS
            def set_powermax(inst):
                inst.power = inst.maximum_power
            laser640__powermax = self.findChild((QWidget, ), 'laser640__powermax')
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
    
            focus_lock_on.clicked.connect(handletoggle)
