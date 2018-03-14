# import from python library
import sys
import os
import threading
import time

# import updatethread from the updatethread.py file in this folder
from updateThread import UpdateThread

# import all the neccessary PyQt5 modules - requires PyQt5
from PyQt5.QtCore import QUrl, QObject, QVariant, QRunnable, QCoreApplication, QThreadPool, pyqtSignal
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtGui import QColor
from PyQt5.QtQuick import QQuickView

# define the main window
class MainWindow(QQuickView): 

	def __init__(self,parent=None):

		# initialize the main window and set the structure source to be the view.qml file
		super(MainWindow, self).__init__(parent)
		self.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__),'view.qml'))) 
		self.qml = self.rootObject()

		# run the updateThread which feeds info to the UI
		self.setupUpdateThread() 

	# the following functions set the QML properties
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

	# the updateThread runs parellel to the UI
	def setupUpdateThread(self):  

		self.updateThread = UpdateThread()  

		# connect the updateThread's properties to the windows update functions
		self.updateThread.speed.connect(self.updateSpeed)
		self.updateThread.gear.connect(self.updateGear)
		self.updateThread.rpm.connect(self.updateRpm)
		self.updateThread.statusText.connect(self.updateStatusText)
		self.updateThread.statusColor.connect(self.updateStatusColor)
		self.updateThread.fuelPercent.connect(self.updateFuelPercent)
		self.updateThread.chargePercent.connect(self.updateChargePercent)
  
  		# run the updateThread
		if not self.updateThread.isRunning():
			
			self.updateThread.start() 

# if the main window has been defined
if __name__ == '__main__':  

	# create a new window
	app = QGuiApplication(sys.argv)  
	win = MainWindow()  

	# show the window (.show() or .showFullScreen())
	win.show()  

	# run the events in the window (initalize)
	app.processEvents()

	# after events have been run close the window (doesn't happen naturally because it continuously updates)
	sys.exit(app.exec_())
