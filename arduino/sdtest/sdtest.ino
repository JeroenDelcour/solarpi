#include <SPI.h>
#include <SD.h>

int chipSelect = 4; //chipSelect pin for the SD card Reader
File dataFile;

void setup() {
    // Open serial communications and wait for port to open:
    Serial.begin(9600);
    while (!Serial) {
        ; // wait for serial port to connect. Needed for native USB port only
    }
    if (!SD.begin(chipSelect)) {
        Serial.println("SD card initialization failed! Is it connected?");
        return;
    }
};

void loop() {

    // Write to the SD card.
    dataFile = SD.open("test.txt", FILE_WRITE);
    if (dataFile) {
        dataFile.println("testing 1,2,3...");
    }
    // if the file isn't open, pop up an error:
    else {
        Serial.println("Error opening test.txt");
    }
    dataFile.close();

    delay(1000);
}
