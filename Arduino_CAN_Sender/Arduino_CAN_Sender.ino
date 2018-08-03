// Include library to talk to CAN shield
#include <mcp_can.h>
#include <SPI.h>

// Define the input pin and CAN Shield select pin
#define SPI_CS_PIN 9

// Initialize with the CAN Shield select pin
MCP_CAN CAN(SPI_CS_PIN);

void setup() {

  // Start the serial stream
  Serial.begin(9600);

  // Initialize the CAN Bus and check for errors
  while (CAN_OK != CAN.begin(CAN_500KBPS))
  {
      Serial.println("CAN BUS Shield init fail");
      Serial.println("Init CAN BUS Shield again");
      delay(100);
  }

  Serial.println("CAN BUS Shield init ok!");
  
}

int rpm = 2400;
bool goingup = true;
byte groundspeed = 0; 
byte gear = 1;
byte fuel = 100;
byte charge = 100;

void loop() {

  // if the RPM is too high, go down
  if(rpm > 10000) goingup = false;
  else if(rpm < 2400) goingup = true;

  // if we're going up raise the RPM
  if(goingup) rpm+=200;
  else rpm-=200;

  groundspeed = rpm/150;
  gear = rpm/2000;
  fuel = 7/760.0*rpm+55.0/19;
  charge = -1/80.0*rpm+130;

  byte id_1520[8] = {0, 0, 0, 0, 0, 0, rpm>>8, rpm&0xFF};
  byte id_257[8] = {0, 0, 0, 0, groundspeed, charge, gear&0xF, 0};
  byte id_258[8] = {0, 0, 0, 0, fuel, 0, 0, 0};

  // Send the message over CAN to the same places they're sent on the car. See https://docs.google.com/spreadsheets/d/1sYD5FM78nsb_uLSUSBNHb7dAY1rldME3raeu9eHfI0A/edit?usp=sharing
  CAN.sendMsgBuf(1520, 0, 8, id_1520);
  CAN.sendMsgBuf(257, 0, 8, id_257);
  CAN.sendMsgBuf(258, 0, 8, id_258);
  
  // Delay before sending the next signal
  delay(100);

}
