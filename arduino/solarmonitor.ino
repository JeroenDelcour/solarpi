#include <Wire.h>
#include <Adafruit_INA219.h>
#include <SD.h>
#include <LowPower.h>

const int chipSelect = 4;
Adafruit_INA219 ina219(0x41);

void setup() {
  analogReference(INTERNAL);
  
  Serial.begin(9600);
  Serial.println("Hello!");
  uint32_t currentFrequency;
  
  // Initialize the INA219.
  // By default the initialization will use the largest range (32V, 2A).  However
  // you can call a setCalibration function to change this range (see comments).
  ina219.begin();
  // To use a slightly lower 32V, 1A range (higher precision on amps):
  //ina219.setCalibration_32V_1A();
  // Or to use a lower 16V, 400mA range (higher precision on volts and amps):
  //ina219.setCalibration_16V_400mA();
  Serial.println("Measuring voltage and current with INA219 ...");
  
  Serial.print("Initializing SD card...");
  // make sure that the default chip select pin is set to
  // output, even if you don't use it:
  pinMode(10, OUTPUT);
  
  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    return;
  }
  Serial.println("card initialized.");
}

float read_V_in() {
  // read battery voltage through voltage divider
  // V_out = V_in * R_2 / (R_1 + R_2)
  // V_in = V_out / (R_2 / (R_1 + R_2)
  int sensorValue = analogRead(A3);
  float v_out = sensorValue * (1.1 / 1023.0);
  float v_in = v_out / (325.0 / 1975.0);
  return v_in;
}

void loop() 
{
  float shuntvoltage = 0;
  float busvoltage = 0;
  float current_mA = 0;
  float loadvoltage = 0;
  float power_mW = 0;
  float batteryvoltage = 0;

  shuntvoltage = ina219.getShuntVoltage_mV();
  busvoltage = ina219.getBusVoltage_V();
  current_mA = ina219.getCurrent_mA();
  power_mW = ina219.getPower_mW();
  loadvoltage = busvoltage + (shuntvoltage / 1000);
  batteryvoltage = read_V_in();
  
  Serial.print("Bus Voltage:   "); Serial.print(busvoltage); Serial.println(" V");
  Serial.print("Shunt Voltage: "); Serial.print(shuntvoltage); Serial.println(" mV");
  Serial.print("Load Voltage:  "); Serial.print(loadvoltage); Serial.println(" V");
  Serial.print("Current:       "); Serial.print(current_mA); Serial.println(" mA");
  Serial.print("Power:         "); Serial.print(power_mW); Serial.println(" mW");
  Serial.print("V divider:     "); Serial.print(batteryvoltage); Serial.println(" V");
  Serial.println("");

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  File dataFile = SD.open("datalog.csv", FILE_WRITE);

  // if the file is available, write to it:
  if (dataFile) {
    dataFile.print(shuntvoltage); dataFile.print(",");
    dataFile.print(busvoltage); dataFile.print(",");
    dataFile.print(current_mA); dataFile.print(",");
    dataFile.print(power_mW); dataFile.print(",");
    dataFile.print(loadvoltage); dataFile.print(",");
    dataFile.print(batteryvoltage); dataFile.println("");
    dataFile.close();
  }  
  // if the file isn't open, pop up an error:
  else {
    Serial.println("error opening datalog.csv");
  } 

  //delay(2000);
  LowPower.powerDown(SLEEP_2S, ADC_OFF, BOD_OFF);
}
