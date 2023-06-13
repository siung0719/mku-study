/*******************************************************************************
* Copyright 2016 ROBOTIS CO., LTD.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

#include <Dynamixel2Arduino.h>

#define DXL_SERIAL   Serial1 //OpenCM9.04 EXP Board's DXL port Serial. (Serial1 for the DXL port on the OpenCM 9.04 board)
#define DEBUG_SERIAL Serial
const int DXL_DIR_PIN = 28; //OpenCM9.04 EXP Board's DIR PIN. (28 for the DXL port on the OpenCM 9.04 board)
String cmd;
const uint8_t Dp=1;
const uint8_t Dt=3;
const float DXL_PROTOCOL_VERSION = 1.0;

float pm=120;
float tm=90;

float s1;
float s2;
Dynamixel2Arduino dxl(DXL_SERIAL, DXL_DIR_PIN);

//This namespace is required to use Control table item names
using namespace ControlTableItem;

void setup() {
  // put your setup code here, to run once:
  
  // Use UART port of DYNAMIXEL Shield to debug.
  DEBUG_SERIAL.begin(115200);
  while(!DEBUG_SERIAL);

  // Set Port baudrate to 57600bps. This has to match with DYNAMIXEL baudrate.
  dxl.begin(1000000);
  // Set Port Protocol Version. This has to match with DYNAMIXEL protocol version.
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);

  // Turn off torque when configuring items in EEPROM area
  dxl.torqueOff(Dp);
  dxl.setOperatingMode(Dp, OP_POSITION);
  dxl.torqueOn(Dp);

  dxl.torqueOff(Dt);
  dxl.setOperatingMode(Dt, OP_POSITION);
  dxl.torqueOn(Dt);
  // Limit the maximum velocity in Position Control Mode. Use 0 for Max speed
  dxl.writeControlTableItem(PROFILE_VELOCITY, Dt, 30);
  dxl.writeControlTableItem(PROFILE_VELOCITY, Dp, 30);

  dxl.setGoalPosition(Dp,map(pm,0,180,0,1023));
  dxl.setGoalPosition(Dt,map(tm,0,180,0,1023));
}

void loop() {
  // put your main code here, to run repeatedly:
  
  // Please refer to e-Manual(http://emanual.robotis.com/docs/en/parts/interface/dynamixel_shield/) for available range of value. 
  // Set Goal Position in RAW value
  if(Serial.available()>0)
  {
    cmd=Serial.readStringUntil('\n');
    int f=cmd.indexOf("t");
    if(cmd.substring(0,1)=="p")
    {
      s1=cmd.substring(1,f).toFloat();
      s2=cmd.substring(f+1).toFloat();
      pm=pm+s1/10;
      tm=tm+s2/10;
    }
  }
  pm = constrain(pm, 40, 140); // set new pan position, limited to 40-140
  tm = constrain(tm, 70, 180);

  dxl.setGoalPosition(Dp,map(pm,0,180,0,1023));
  dxl.setGoalPosition(Dt,map(tm,0,180,0,1023));
  delay(100);

}
