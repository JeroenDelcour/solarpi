#include <SPI.h>
#include <SD.h>

const int chipSelect = 4;
File dataFile;

struct datastore {
    uint16_t adc1;
    uint16_t adc2;
    float voltage;
    float current;
};

void setup() {
    Serial.begin(9600);
    Serial.print("Initializing SD card...");
    pinMode(10, OUTPUT);

    if (!SD.begin(chipSelect)) {
        Serial.println("Card failed, or not present");
        return;
    }

    Serial.println("card initialized.");
    dataFile = SD.open("datalog.dat", FILE_WRITE);
}

void loop() {
    struct datastore myData;
    myData.adc1 = analogRead(0);
    myData.adc2 = analogRead(1);
    myData.voltage = myData.adc1 / 1023.0 * 5.0;
    myData.current = myData.adc2 / 10000.0 * 23.4429;
    dataFile.write((const uint8_t *)&myData, sizeof(myData));
    delay(50);
}
