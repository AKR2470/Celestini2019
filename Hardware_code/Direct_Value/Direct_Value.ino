double val = 0;
void setup() {
 pinMode(4, INPUT);
 Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(0);
  val = analogRead(4);
  Serial.println(val);
}
