# import python system modules
import time
import math
from random import randint

# import relevant PyQT5 modules
from PyQt5.QtCore import QThread, pyqtSignal

# import the paho-mqtt module to communicate with the MQTT server
import paho.mqtt.client as mqtt

#defines the updateThread class and all functions
class UpdateThread(QThread):
	
	# provides signals that will push to functions in wherever the updateThead object is created
	gear = pyqtSignal(str)
	speed = pyqtSignal(str)
	rpm = pyqtSignal(int)
	statusText = pyqtSignal(str)
	statusColor = pyqtSignal(str)
	chargePercent = pyqtSignal(int)
	fuelPercent = pyqtSignal(int)

	# initialize the updateThread
	def __init__(self,parent=None):  

		super(UpdateThread,self).__init__(parent)  
		self.exiting = False
	
	def __del__(self):

		self.wait()

	def stop(self):

		self.exiting = True
		self.terminate()

	# set run behaviour to the checkForUpdates thread
	def run(self):

		while not self.exiting:

			self.checkForUpdates()

		return 

	# defines the check for updates thread
	def checkForUpdates(self):

		# connect to the MQTT client
		broker_address="127.0.0.1"
		client=mqtt.Client("Mosquitto Teleserver")
		try:
			client.connect(broker_address)
		except ConnectionRefusedError:
			self.statusText.emit(str("SRVR"))
			self.statusColor.emit(str("red"))

		# pause before animating
		time.sleep(2)

		# reset everything to start
		self.statusText.emit(str("OK"))
		self.statusColor.emit(str("#07DD07"))
		self.fuelPercent.emit(int(100))
		self.chargePercent.emit(int(100))

		# change rpm, speed, and gear through a range
		x = -150
		while x <= 150:

			# push data to UI
			self.rpm.emit(int(x))
			self.speed.emit(str(math.ceil((x+150)/3)))
			self.gear.emit(str(math.ceil((x+150)/60)))

			# push data to MQTT server
			client.publish("car/rpm",x)
			client.publish("car/speed",math.ceil((x+150)/3))
			client.publish("car/gear",math.ceil((x+150)/60))

			# slow down animation execution
			time.sleep(.02)
			x+=1

		#change fuel percent through a range, send to UI, and push to MQTT
		x = 100
		while x >= 25:
			self.fuelPercent.emit(int(x))
			client.publish("car/fuelPercent",x)
			time.sleep(.05)
			x-=1

		# demonstrate the low fuel status
		self.statusText.emit(str("FUEL"))
		self.statusColor.emit(str("red"))

		# change charge percent through a range, send to UI, and push to MQTT
		x = 100
		while x >= 25:
			self.chargePercent.emit(int(x))
			client.publish("car/chargePercent",x)
			time.sleep(.05)
			x-=1

		# demonstrate the low battery status
		self.statusText.emit(str("BATT"))

		# wait and then demonstrate a hot engine warning
		time.sleep(1)
		self.statusText.emit(str("HOT"))

		# wait before looping again
		time.sleep(2)