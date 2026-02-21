int fanPin = 9;
int temp;
bool fanOn = false;

#define ON_TEMP  65
#define OFF_TEMP 55

void setup() {
  Serial.begin(9600);
  //Serial.setTimeout(100);
  pinMode(fanPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    temp = Serial.parseInt(SKIP_NONE);
    //Serial.println("Received: ");
    // Serial.println(temp);
    if (temp != 0) {
        if (!fanOn && temp >= ON_TEMP) {
        fanOn = true;
        digitalWrite(fanPin, HIGH);
        Serial.println("Fans ON");
      }
      else if (fanOn && temp <= OFF_TEMP) {
        fanOn = false;
        digitalWrite(fanPin, LOW);
        Serial.println("Fans OFF");
      }
      else {
        Serial.println("No change");
      }
    }
  }
}

/*

*/

