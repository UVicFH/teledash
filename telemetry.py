# imports from general python
import os
import time
from datetime import datetime

# requires pip install of paho-mqtt, python-can, and cantools
import paho.mqtt.client as mqtt
import can
import cantools

# import object from custom class
from mosquitto_sender import Mosquitto_Sender

# create a global for counting messages received as a heartbeat and output it every timeDif
messagesReceived = 0
updateInterval = 500
lastUpdate = 0

print("Creating and opening datalog file")
dateTimeObj = datetime.now()
dateTimeString = str(dateTimeObj).replace(":", ".")
datalog = open("/mnt/USB/datalog/log" + dateTimeString + ".txt","w+")

print("Loading CAN database...\n")
datalog.write("Loading CAN database...\r\n")
db = cantools.database.load_file('/mnt/USB/Database.dbc')
print(db.messages)
datalog.write(str(db.messages))
print("\n\n")
datalog.write("\r\n\r\n")

print("Attaching to CAN bus...\n")
datalog.write("Attaching to CAN bus...\r\n")
bus=can.interface.Bus(channel='can0', bustype='socketcan_native')

print("Connecting to MQTT server...\n")
datalog.write("Connecting to MQTT server...\r\n")
mqttSender = Mosquitto_Sender()
mqttSender.connect("192.168.1.41")
mqttSender.start_handler()

print("In response mode\n")
datalog.write("In response mode\r\n")
while(1):

    loopTime = int(time.time()*1000)

    message = bus.recv(0.1)
    messageName = "NoNameFound"

    if(message == None):
        print("No message received after 100ms\n")
        datalog.write("No message received after 100ms\r\n")
    else:

        messagesReceived = messagesReceived + 1

        try:
            decoded = str(db.decode_message(message.arbitration_id, message.data))
            decoded.replace("'", "\"")
        except:
            "Message ID: " + str(message.arbitration_id) + " not found in database and not recorded"
            decoded = '{"none": 0}'

        try:
            messageInDB = db.get_message_by_frame_id(message.arbitration_id)
            messageName = messageInDB.name
        except:
            messageName = "Unknown"

        # print(decoded + "\n")
        jsonString = '\'{"'+ messageName + '":' + decoded + '}\''
        mqttSender.send("hybrid/" + messageName, jsonString)
        datalog.write(jsonString + "\r\n")

    if(loopTime - lastUpdate > updateInterval):

        lastUpdate = loopTime
        print("Messages Received: " + str(messagesReceived) + "\r\n")
