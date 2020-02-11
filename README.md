# teledash
Telemetry integrated infotainment system that automatically processes data using a DBC file.

## Getting Started
Very little is required to get started with this project. It is designed to run on a raspberry pi so setup instructions will be given below for this platform but it can theoretically work with any CAN interface on a computer running Python. 

### Hardware
This project is designed to be run on a Raspberry Pi 3 B. It is designed for the MCP2515 and MCP2552 chips. The setup for these chips to create a CAN bus will be given below. This setup assumed that the interrupt pin goes to pin 25 on the GPIO and the bus runs at 500kbps. It is also designed to be run with a 5GHz USB wifi dongle using the RTL8812au chip and a USB stick that holds this repo. That way the code and CAN DBC file can be updated by removing the USB stick. Logged data can also be removed this way. 



### Software

#### CAN
To setup the hardware on the Pi run `sudo ./raspi-config` and enable SPI communication. Then make sure you run `sudo apt-get update ` `sudo apt-get upgrade` `sudo reboot` to get the latest versions when installing packages.  We then need to modify the confix file to add the overlay for this chip. Use `sudo nano /boot/config.txt` to edit the file. Add these three lines to the end: 

```
dtparam=spi=on 
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25 
dtoverlay=spi-bcm2835-overlay
```

Reboot the pi with `sudo reboot`. The CAN interface can be brought up with `sudo /sbin/ip link set can0 up type can bitrate 500000`. To make it easier you may want to bring up this interface whenever the Pi boots. This can be done by modifiying the rc.local file (`sudo nano /etc/rc.local`) to append that previous link set command. 

#### Python and libraries
There are many guides available for installing python3, pip3, and libraries so only a short summary will be given here. The three required libraries are [python-can](https://pypi.org/project/python-can/), [cantools](https://pypi.org/project/cantools/), and [paho-mqtt](https://pypi.org/project/paho-mqtt/). 

#### Wifi Dongle
The original hardware also runs on 5GHz wifi using a RTL8812au USB wifi dongle. Any dongle with RTL8812au or RTL8811au will work. The best driver for this chip that we've tested is found here: https://github.com/aircrack-ng/rtl8812au. 

#### Automount USB
[This guide](https://www.raspberrypi.org/documentation/configuration/external-storage.md) was followed to automatically mount the USB drive at /mnt/USB/ and must be replicated to ensure code functionality. 

#### Autorun program
It is most conventient to autorun this program by appending the following line to the `/etc/rc.local` file: 

```
python3 /mnt/USB/telemetry.py
```
