from PyQt5.QtCore import QThread, pyqtSignal
from random import randint
import time
import math

import paho.mqtt.client as mqtt

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

#		broker_address="192.168.1.65"
#		client =mqtt.Client("Mosquitto Teleserver")
#		try:
#			client.connect(broker_address)
#		except ConnectionRefusedError:
#			self.statusText.emit(str("SRVR"))
#			self.statusColor.emit(str("red"))

		time.sleep(5)

		self.statusText.emit(str("OK"))
		self.statusColor.emit(str("#07DD07"))
		self.fuelPercent.emit(int(100))
		self.chargePercent.emit(int(100))

		x = -150
		while x < 150:
			self.rpm.emit(int(x))
			self.speed.emit(str(math.ceil((x+150)/3)))
			self.gear.emit(str(math.ceil((x+150)/60)))
#			client.publish("car/rpm",x)
			time.sleep(.02)
			x+=1

		x = 100
		while x > 25:
			self.fuelPercent.emit(int(x))
			time.sleep(.05)
			x-=1

		self.statusText.emit(str("FUEL"))
		self.statusColor.emit(str("red"))

		x = 100
		while x > 25:
			self.chargePercent.emit(int(x))
			time.sleep(.05)
			x-=1

		self.statusText.emit(str("BATT"))
		time.sleep(1)

		self.statusText.emit(str("HOT"))

		time.sleep(5)