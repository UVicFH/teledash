import paho.mqtt.client as mqtt
import time

class Mosquitto_Sender():
	
	# function called on initialization
	def __init__(self):

		# create a new client object
		self.client = mqtt.Client()
		self.client.reconnect_delay_set(1, 3)
		self.client.on_disconnect = self.on_disconnect

	def connect(self, server, port=1883, keepalive = 60):

		# save the server address
		self.server = server
		self.port = port
		self.keepalive = keepalive

		# connect to the server
		try:
			self.client.connect(self.server, self.port, self.keepalive)
			self.connection_success = True
		
		except:
			self.connection_success = False

	def retry_connect(self):

		# reconnect to the server using existing parameters
		try:
			self.client.connect(self.server, self.port, self.keepalive)
			self.connection_success = True
		except:
			self.connection_success = False

	# send a message with a timestamp so data can be easily mined later
	def send(self, topic, payload=None):

		self.client.publish(topic, payload)

	def on_disconnect(self, client, userdata, rc=0):

		self.connection_success = False

	def start_handler(self):
		self.client.loop_start()

# Here is an example script of how to know the if the connection has been made and send data to it #
# ################################################################################################ #
#
#
# sender = mosquitto_sender()
# sender.connect("test.mosquitto.org")
# sender.start_handler()
#
# i = 0
# while True:
# 	if(sender.connection_success):
#
# 		print("Initial Connection Established " + str(i))
#
# 		# send commands
# 		sender.send("hybrid/test", str(time.time()) + ":" + str(i))
# 		i+=1
# 		time.sleep(1/50)
#
# 	else:
# 		print("Initial Connection Not Established")
# 		time.sleep(1)
# 		sender.retry_connect()