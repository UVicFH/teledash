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

  byte sendrpm[2] = {rpm>>8 & 0xFF, rpm & 0xFF};

  Serial.print("RPM:");
  Serial.print(sendrpm[0]<<8 | sendrpm[1]);
  Serial.print("\tSpeed:");
  Serial.print(groundspeed);
  Serial.print("\tGear:");
  Serial.print(gear);
  Serial.print("\tFuel:");
  Serial.print(fuel);
  Serial.print("\tCharge:");
  Serial.println(charge);

  // Send the message over CAN
  CAN.sendMsgBuf(1512, 0, 2, sendrpm);
  CAN.sendMsgBuf(1513, 0, 1, &groundspeed);
  CAN.sendMsgBuf(1514, 0, 1, &gear);
  CAN.sendMsgBuf(1515, 0, 1, &fuel);
  CAN.sendMsgBuf(1516, 0, 1, &charge);
  
  // Delay before sending the next signal
  delay(100);

}
