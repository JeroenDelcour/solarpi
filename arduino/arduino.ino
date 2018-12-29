int pi_poweroff_pin = 4;
int pi_shutdown_pin = 3;
int pi_reset_pin = 9;

void setup() {
  analogReference(INTERNAL);
  
  pinMode(pi_poweroff_pin, INPUT);
  pinMode(pi_shutdown_pin, OUTPUT);
  pinMode(pi_reset_pin, OUTPUT);
  
  Serial.begin(9600);
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

void shutdown_pi() {
  digitalWrite(pi_shutdown_pin, LOW);
  delay(10);
  digitalWrite(pi_shutdown_pin, HIGH);
}

void reset_pi() {
  digitalWrite(pi_reset_pin, HIGH);
  delay(10);
  digitalWrite(pi_reset_pin, LOW);
  // give Pi some time to boot and pull pi_poweroff_pin HIGH
  delay(10000);
}

void loop() {
    float v_in = read_V_in();
    Serial.print("Supply voltage: "); Serial.println(v_in);
    
    if (v_in < 3.0) {
      Serial.println("Supply voltage below threshold: shutting down Pi.");
      shutdown_pi();
    } else if ((digitalRead(pi_poweroff_pin) == 0) && (v_in > 3.5)) {
      Serial.println("Supply voltage above threshold: resetting Pi.");
      reset_pi();
    }
    
    delay(10000);
}
