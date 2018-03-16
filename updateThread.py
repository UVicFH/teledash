# import from python library
from random import randint
import time
import math

# import all the neccessary PyQt5 modules - requires PyQt5
from PyQt5.QtCore import QThread, pyqtSignal

# import neccesssary mqtt module - requires paho-mqtt
import paho.mqtt.client as mqtt

# import can - requires python-can
import can

# create a can bus on the can0 interface
# requires interface be set up before opening as detailed here (done on Pi already): http://skpang.co.uk/blog/archives/1220
# you may need to "bring up" the interface first with: sudo /sbin/ip link set can0 up type can bitrate 500000
# ^ not yet tested without doing this - if required will need to be automated
import os
os.system('sudo ./set_up_can.sh')
print("If RETLINK answered 'Device or resource busy' don't worry.")
bus=can.interface.Bus(channel='can0', bustype='socketcan_native')

import arbitration_ids

MSTIMEOUT = 100 # in milliseconds

class UpdateThread(QThread):

	# create signals that can be linked to update functions for the UI
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
		
		# recieve a message on the bus and timeout after MSTIMEOUT ms, in which case the gui will show a timeout
		message = bus.recv(MSTIMEOUT/1000)

		if message is None: # bus timed out
			# set the statusText to TIMED OUT and red
			self.statusColor.emit("#DD0707")
			self.statusText.emit("T/O")
			return None
		else:
			# set the statusText to ok and green
			self.statusText.emit(str("OK"))
			self.statusColor.emit(str("#07DD07"))

		if message.arbitration_id == arbitration_ids.rpm:

			# rpm is sent as two bits which needs to be combined again after
			rpm = message.data[0]<<8 | message.data[0]

			# rpmAngle is what is sent to the UI current which is from -150 to 150 corresponding to 0 to 12000
			rpmAngle = int(rpm/40.0-150.0)
			self.rpm.emit(rpmAngle)

		# the rest of these are strightforward

		elif message.arbitration_id == arbitration_ids.speed:
			self.speed.emit(str(message.data[0])) # speed is is a string

		elif message.arbitration_id == arbitration_ids.gear:
			self.gear.emit(str(message.data[0])) # gear is a string

		elif message.arbitration_id == arbitration_ids.charge:
			self.chargePercent.emit(message.data[0]) # chargePercent is an integer
		
		elif message.arbitration_id == arbitration_ids.fuel:
			self.fuelPercent.emit(message.data[0]) # fuelPercent is an integer
		
		

