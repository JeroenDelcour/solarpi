
#include <avr/sleep.h>
#include <avr/power.h>
#include <avr/wdt.h>
#include <Wire.h>
#include <Adafruit_INA219.h>
#include <SD.h>

// Data logging configuration.
#define LOGGING_FREQ_SECONDS   60       // Seconds to wait before a new sensor reading is logged.

#define SERVER_IP              192, 168, 1, 105    // Logging server IP address.  Note that this
                                                   // should be separated with commas and NOT periods!

#define SERVER_PORT            8000                // Logging server listening port.
                                                   
#define MAX_SLEEP_ITERATIONS   LOGGING_FREQ_SECONDS / 8  // Number of times to sleep (for 8 seconds) before
                                                         // a sensor reading is taken and sent to the server.
                                                         // Don't change this unless you also change the 
                                                         // watchdog timer configuration.
                                                         
Adafruit_INA219 ina219_bat;
Adafruit_INA219 ina219_sol;

// On the Ethernet Shield, CS is pin 4. Note that even if it's not
// used as the CS pin, the hardware CS pin (10 on most Arduino boards,
// 53 on the Mega) must be left as an output or the SD library
// functions will not work.
const int chipSelect = 10;

// Internal state used by the sketch.
int sleepIterations = 0;
volatile bool watchdogActivated = false;

// Define watchdog timer interrupt.
ISR(WDT_vect)
{
  // Set the watchdog activated flag.
  // Note that you shouldn't do much work inside an interrupt handler.
  watchdogActivated = true;
}

// Put the Arduino to sleep.
void sleep()
{
  // Set sleep to full power down.  Only external interrupts or 
  // the watchdog timer can wake the CPU!
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);

  // Turn off the ADC while asleep.
  power_adc_disable();

  // Enable sleep and enter sleep mode.
  sleep_mode();

  // CPU is now asleep and program execution completely halts!
  // Once awake, execution will resume at this point.
  
  // When awake, disable sleep mode and turn on all devices.
  sleep_disable();
  power_all_enable();
}

// Take a sensor reading and write it to the microSD card.
void logSensorReading() {
  
  float shuntvoltage_bat = 0;
  float busvoltage_bat = 0;
  float current_mA_bat = 0;
  float loadvoltage_bat = 0;
  shuntvoltage_bat = ina219_bat.getShuntVoltage_mV();
  busvoltage_bat = ina219_bat.getBusVoltage_V();
  current_mA_bat = ina219_bat.getCurrent_mA();
  loadvoltage_bat = busvoltage_bat + (shuntvoltage_bat / 1000);
  
  float shuntvoltage_sol = 0;
  float busvoltage_sol = 0;
  float current_mA_sol = 0;
  float loadvoltage_sol = 0;
  shuntvoltage_sol = ina219_sol.getShuntVoltage_mV();
  busvoltage_sol = ina219_sol.getBusVoltage_V();
  current_mA_sol = ina219_sol.getCurrent_mA();
  loadvoltage_sol = busvoltage_sol + (shuntvoltage_sol / 1000);
  
  File dataFile = SD.open("datalog.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.print(loadvoltage_bat); dataFile.print(",");
    dataFile.print(current_mA_bat); dataFile.print(",");
    dataFile.print(loadvoltage_sol); dataFile.print(",");
    dataFile.println(current_mA_sol);
    dataFile.close();
  }
}

void setup(void)
{  
  Serial.begin(9600);
  
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
  
  uint32_t currentFrequency;
  
  // Initialize the INA219.
  // By default the initialization will use the largest range (32V, 2A).  However
  // you can call a setCalibration function to change this range (see comments).
  ina219_bat.begin();
  ina219_sol.begin();
  // To use a slightly lower 32V, 1A range (higher precision on amps):
  //ina219.setCalibration_32V_1A();
  // Or to use a lower 16V, 400mA range (higher precision on volts and amps):
  //ina219.setCalibration_16V_400mA();
 
 
  // Setup the watchdog timer to run an interrupt which
  // wakes the Arduino from sleep every 8 seconds.
  
  // Note that the default behavior of resetting the Arduino
  // with the watchdog will be disabled.
  
  // This next section of code is timing critical, so interrupts are disabled.
  // See more details of how to change the watchdog in the ATmega328P datasheet
  // around page 50, Watchdog Timer.
  noInterrupts();
  
  // Set the watchdog reset bit in the MCU status register to 0.
  MCUSR &= ~(1<<WDRF);
  
  // Set WDCE and WDE bits in the watchdog control register.
  WDTCSR |= (1<<WDCE) | (1<<WDE);

  // Set watchdog clock prescaler bits to a value of 8 seconds.
  WDTCSR = (1<<WDP0) | (1<<WDP3);
  
  // Enable watchdog as interrupt only (no reset).
  WDTCSR |= (1<<WDIE);
  
  // Enable interrupts again.
  interrupts();
  
  // Initialize log file if it doesn't exist
  if (!SD.exists("datalog.csv")) {
    File dataFile = SD.open("datalog.txt", FILE_WRITE);
    if (dataFile) {
      dataFile.println("battery_V,battery_mA,solar_V,solar_mA"); // header
      dataFile.close();
    }
    // if the file isn't open, pop up an error:
    else {
      Serial.println("error opening datalog.txt");
    } 
  }
  
  Serial.println(F("Setup complete."));
}

void loop(void)
{
  // Don't do anything unless the watchdog timer interrupt has fired.
  if (watchdogActivated)
  {
    watchdogActivated = false;
    // Increase the count of sleep iterations and take a sensor
    // reading once the max number of iterations has been hit.
    sleepIterations += 1;
    if (sleepIterations >= MAX_SLEEP_ITERATIONS) {
      // Reset the number of sleep iterations.
      sleepIterations = 0;
      // Log the sensor data
      logSensorReading();
    }
  }
  
  // Go to sleep!
  sleep();
}

