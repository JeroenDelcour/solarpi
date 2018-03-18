#include <SPI.h>
#include <SD.h>
#include <Wire.h>
#include <Adafruit_INA219.h>
#include <TimeLib.h>

File dataFile;
Adafruit_INA219 ina219;

struct datastore {
  time_t t;
  float voltage;
  float current;
};

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }


  if (!SD.begin(4)) {
    Serial.println("SD card failed, or not present!");
    return;
  }

  // Initialize the INA219.
  // By default the initialization will use the largest range (32V, 2A).  However
  // you can call a setCalibration function to change this range (see comments).
  // To use a slightly lower 32V, 1A range (higher precision on amps):
  //ina219.setCalibration_32V_1A();
  // Or to use a lower 16V, 400mA range (higher precision on volts and amps):
  //ina219.setCalibration_16V_400mA();
  ina219.begin();
};

void loop() {
  struct datastore myData;

  myData.t = now();
  myData.voltage = ina219.getBusVoltage_V();
  myData.current = ina219.getCurrent_mA();

  Serial.print("Bus Voltage:   "); Serial.print(myData.voltage); Serial.println(" V");
  Serial.print("Current:       "); Serial.print(myData.current); Serial.println(" mA");

  // Write to the SD card.
  // "&myData" gets the address in memory where the data is stored. It's a
  // "struct datastore *" type, so we need to cast it to an unsigned byte pointer
  // type by prepending it with "(const uint8_t *)" so the write funcion sees it
  // as an array of bytes.
  dataFile.write((const uint8_t *)&myData, sizeof(myData));

  delay(1000);
}
