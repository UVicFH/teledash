from PyQt5.QtCore import QThread, pyqtSignal
from random import randint
import time
import math

import paho.mqtt.client as mqtt
import can

bus=can.interface.Bus(channel='can0', bustype='socketcan_native')

class UpdateThread(QThread):

	gear = pyqtSignal(str)
	speed = pyqtSignal(str)
	rpm = pyqtSignal(int)
	statusText = pyqtSignal(str)
	statusColor = pyqtSignal(str)
	chargePercent = pyqtSignal(int)
	fuelPercent = pyqtSignal(int)

	def __init__(self,parent=None):

		super(UpdateThread,self).__init__(parent)
		self.exiting = False

	def __del__(self):

		self.wait()

	def stop(self):

		self.exiting = True
		self.terminate()

	def run(self):

		while not self.exiting:

			self.checkForUpdates()

		return

	def checkForUpdates(self):

		self.statusText.emit(str("OK"))
		self.statusColor.emit(str("#07DD07"))
		self.fuelPercent.emit(int(100))
		self.chargePercent.emit(int(100))

		message = bus.recv(1)
		if(message.arbitration_id == 1512):
			rpm = message.data[0]<<8 | message.data[0]
			rpmAngle = int(rpm/40.0-150.0)
			self.rpm.emit(rpmAngle)

