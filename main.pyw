# import python system modules
import sys
import os
import threading
import time

# import the updateThread process
from updateThread import UpdateThread

# import relevant PyQT5 modules
from PyQt5.QtCore import QUrl, QObject, QVariant, QRunnable, QCoreApplication, QThreadPool, pyqtSignal
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtGui import QColor
from PyQt5.QtQuick import QQuickView

# define the main window and its function
class MainWindow(QQuickView): 

	# initialization function
	def __init__(self,parent=None):

		# initialize the container
		super(MainWindow, self).__init__(parent)

		# set the source to the view.qml file
		self.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__),'view.qml'))) 
		self.qml = self.rootObject()
		
		# setup the update thread
		self.setupUpdateThread() 

	# create functions that will set qml properties for each displayed variable
	def updateSpeed(self, speed):
		self.qml.setProperty("speed", speed)

	def updateGear(self, gear):
		self.qml.setProperty("gear", gear)

	def updateStatusText(self, statusText):
		self.qml.setProperty("statustext", statusText)

	def updateStatusColor(self, statusColor):
		self.qml.setProperty("statuscolor", statusColor)

	def updateChargePercent(self, chargePercent):
		self.qml.setProperty("chargepercent", chargePercent)

	def updateFuelPercent(self, fuelPercent):
		self.qml.setProperty("fuelpercent", fuelPercent)

	def updateRpm(self, rpm):
		self.qml.setProperty("rpmAngle", rpm)

	# initialize the updateThread
	def setupUpdateThread(self):  

		# create new updateThread object
		self.updateThread = UpdateThread()

		# connect the updateThead's signals to this window's functions
		self.updateThread.speed.connect(self.updateSpeed)
		self.updateThread.gear.connect(self.updateGear)
		self.updateThread.rpm.connect(self.updateRpm)
		self.updateThread.statusText.connect(self.updateStatusText)
		self.updateThread.statusColor.connect(self.updateStatusColor)
		self.updateThread.fuelPercent.connect(self.updateFuelPercent)
		self.updateThread.chargePercent.connect(self.updateChargePercent)
  		
  		# start the thread assuming it isn't already running
		if not self.updateThread.isRunning():
			
			self.updateThread.start() 

# initialize the window
if __name__ == '__main__':  

	#initialize the application and main window
	app = QGuiApplication(sys.argv)  
	win = MainWindow()  

	# change to win.showFullScreen() for fullscreen; also change pixel size in the qml doc
	win.show()  
	app.processEvents()
	sys.exit(app.exec_())
