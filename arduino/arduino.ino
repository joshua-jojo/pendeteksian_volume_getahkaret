#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 5, 4);
#define trigger 2
#define echo 3

long duration;
int distance;

void setup() {
  Serial.begin(57600);
  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);
  lcd.begin();
}


void loop() {
  String jarak = String(hcsr());
  tampil_lcd("Jarak : " + jarak+" CM");
  Serial.println(hcsr());
  delay(500);
  
}

int tampil_lcd(String data) {
  lcd.setCursor(0, 0);
  lcd.print(data);
}

int hcsr() {
  digitalWrite(trigger, LOW);
  delayMicroseconds(2);
  digitalWrite(trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger, LOW);
  duration = pulseIn(echo, HIGH);
  distance = duration * 0.034 / 2;
  return distance;
}
