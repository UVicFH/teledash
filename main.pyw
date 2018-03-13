import sys
import os
import threading
import time

from updateThread import UpdateThread

from PyQt5.QtCore import QUrl, QObject, QVariant, QRunnable, QCoreApplication, QThreadPool, pyqtSignal
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtGui import QColor
from PyQt5.QtQuick import QQuickView

class MainWindow(QQuickView): 

	def __init__(self,parent=None):

		super(MainWindow, self).__init__(parent)
		self.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__),'view.qml'))) 
		self.qml = self.rootObject()
		self.setupUpdateThread() 

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

	def setupUpdateThread(self):  

		self.updateThread = UpdateThread()  

		self.updateThread.speed.connect(self.updateSpeed)
		self.updateThread.gear.connect(self.updateGear)
		self.updateThread.rpm.connect(self.updateRpm)
		self.updateThread.statusText.connect(self.updateStatusText)
		self.updateThread.statusColor.connect(self.updateStatusColor)
		self.updateThread.fuelPercent.connect(self.updateFuelPercent)
		self.updateThread.chargePercent.connect(self.updateChargePercent)
  
		if not self.updateThread.isRunning():
			
			self.updateThread.start() 

if __name__ == '__main__':  
	app = QGuiApplication(sys.argv)  
	win = MainWindow()  
	win.show()  
	app.processEvents()
	sys.exit(app.exec_())
