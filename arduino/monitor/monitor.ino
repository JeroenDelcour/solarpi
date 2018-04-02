#include <SPI.h>
#include <SD.h>
#include <Wire.h>
#include <Adafruit_INA219.h>
#include <TimeLib.h>

File dataFile;
Adafruit_INA219 ina219_battery(0x41);
Adafruit_INA219 ina219_solar(0x40);

struct datastore {
    time_t time;
    float voltage;
    float current;
};

#define TIME_HEADER  "T"   // Header tag for serial time sync message
#define TIME_REQUEST  7    // ASCII bell character requests a time sync message 

void processSyncMessage() {
    unsigned long pctime;
    const unsigned long DEFAULT_TIME = 1357041600; // Jan 1 2013

    if(Serial.find(TIME_HEADER)) {
        pctime = Serial.parseInt();
        if( pctime >= DEFAULT_TIME) { // check the integer is a valid time (greater than Jan 1 2013)
            setTime(pctime); // Sync Arduino clock to the time received on the serial port
        }
    }
}

time_t requestSync()
{
    Serial.write(TIME_REQUEST);  
    return 0; // the time will be sent later in response to serial mesg
}

void setup() {
    Serial.begin(9600);
    if (!SD.begin(4)) {
        Serial.println("SD card initialization failed! Is it connected?");
        return;
    }
    setSyncProvider( requestSync);  //set function to call when time sync required
    Serial.println("Waiting for time sync message");

    ina219_battery.begin();
    ina219_solar.begin();
};

void loop() {
    if (Serial.available()) {
        processSyncMessage();
    }
    if (timeStatus()!= timeNotSet) {
        struct datastore battery_data;
        struct datastore solar_data;
        battery_data.time = now();
        battery_data.voltage = ina219_battery.getBusVoltage_V();
        battery_data.current = ina219_battery.getCurrent_mA();
        solar_data.time = now();
        solar_data.voltage = ina219_solar.getBusVoltage_V();
        solar_data.current = ina219_solar.getCurrent_mA();

        // Write to the SD card.
        dataFile = SD.open("battery.dat", FILE_WRITE);
        if (dataFile) {
            dataFile.write((const uint8_t *)&battery_data, sizeof(battery_data));
        }
        // if the file isn't open, pop up an error:
        else {
            Serial.println("Error opening battery.dat");
        }
        dataFile.close();
        dataFile = SD.open("solar.dat", FILE_WRITE);
        if (dataFile) {
            dataFile.write((const uint8_t *)&solar_data, sizeof(solar_data));
        }
        // if the file isn't open, pop up an error:
        else {
            Serial.println("Error opening solar.dat");
        }
        dataFile.close();

    }

    delay(1000);
}
