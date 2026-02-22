int fanPin = 9;

#define ON_TEMP  65
#define OFF_TEMP 55
  // Source - https://stackoverflow.com/a/24075787
  // Posted by Peter Gibson, modified by community. See post 'Timeline' for change history
  // Retrieved 2026-02-22, License - CC BY-SA 3.0

void setup() {
  Serial.begin(9600);
  //Serial.setTimeout(100);
  pinMode(fanPin, OUTPUT);
}

void loop() {
  digitalWrite(fanPin, HIGH);
}

/*

*/

