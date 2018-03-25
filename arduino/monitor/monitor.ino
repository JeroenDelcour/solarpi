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

void printDigits(int digits){
    // utility function for digital clock display: prints preceding colon and leading 0
    Serial.print(":");
    if(digits < 10)
        Serial.print('0');
    Serial.print(digits);
}

void setup() {
    // Open serial communications and wait for port to open:
    Serial.begin(9600);
    while (!Serial) {
        ; // wait for serial port to connect. Needed for native USB port only
    }
    if (!SD.begin(4)) {
        Serial.println("SD card initialization failed! Is it connected?");
        return;
    }
    setSyncProvider( requestSync);  //set function to call when time sync required
    Serial.println("Waiting for time sync message");

    ina219_battery.begin();
    ina219_solar.begin();

    // write header
    dataFile = SD.open("battery.csv", FILE_WRITE);
    if (dataFile) {
        dataFile.println("time,voltage (V),current (mA)");
    }
    dataFile.close();
    dataFile = SD.open("solar.csv", FILE_WRITE);
    if (dataFile) {
        dataFile.println("time,voltage (V),current (mA)");
    }
    dataFile.close();
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
//        float shuntvoltage = 0;

        // Print to serial output
//        Serial.print(hour());
//        printDigits(minute());
//        printDigits(second());
//        Serial.print(" ");
//        Serial.print(day());
//        Serial.print(" ");
//        Serial.print(month());
//        Serial.print(" ");
//        Serial.print(year()); 
//        Serial.println();
//        shuntvoltage = ina219_solar.getShuntVoltage_mV();
//        Serial.print("Bus Voltage:   "); Serial.print(solar_data.voltage); Serial.println(" V");
//        Serial.print("Shunt Voltage: "); Serial.print(shuntvoltage); Serial.println(" mV");
//        Serial.print("Load Voltage:  "); Serial.print(solar_data.voltage + (shuntvoltage / 1000)); Serial.println(" V");
//        Serial.print("Current:       "); Serial.print(solar_data.current); Serial.println(" mA");
//        Serial.println("");

        // Write to the SD card.
        dataFile = SD.open("battery.csv", FILE_WRITE);
        if (dataFile) {
            dataFile.print(battery_data.time); dataFile.print(",");
            dataFile.print(battery_data.voltage); dataFile.print(",");
            dataFile.println(battery_data.current);
        }
        // if the file isn't open, pop up an error:
        else {
            Serial.println("Error opening battery.csv");
        }
        dataFile.close();
        dataFile = SD.open("solar.csv", FILE_WRITE);
        if (dataFile) {
            dataFile.print(solar_data.time); dataFile.print(",");
            dataFile.print(solar_data.voltage); dataFile.print(",");
            dataFile.println(solar_data.current);
        }
        // if the file isn't open, pop up an error:
        else {
            Serial.println("Error opening solar.csv");
        }
        dataFile.close();

    }

    delay(1000);
}
