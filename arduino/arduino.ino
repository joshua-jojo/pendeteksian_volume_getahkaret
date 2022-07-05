#include <LiquidCrystal_I2C.h>
#include "HX711.h"
#define DOUT  A0
#define CLK  A1
#define trigger 2
#define echo 3

LiquidCrystal_I2C lcd(0x27, 5, 4);

long duration;
int distance;
HX711 scale(DOUT, CLK);
float calibration_factor = 650;
float final_kalibrasi = 110.00;
int GRAM;

void setup() {
  Serial.begin(115200);
  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);
  lcd.begin();


  scale.set_scale();
  scale.tare();
  long zero_factor = scale.read_average();
  delay(1000);
}


void loop() {
  while (!Serial.available());
  String data = Serial.readStringUntil('\n');
  delay(10);
  tampil_lcd(data);
}

int tampil_lcd(String data) {
  lcd.setCursor(0, 0);
  lcd.print(data);
  delay(100);
  lcd.clear();
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

int kalibrasi_berat() {
  scale.set_scale(calibration_factor);
  GRAM = scale.get_units(), 4;
  Serial.print("Reading: ");
  Serial.print(GRAM);
  Serial.print(" Gram");
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor);
  Serial.println();

  if (Serial.available()) {
    char temp = Serial.read();
    if (temp == '+' || temp == 'a')
      calibration_factor += 0.1;
    else if (temp == '-' || temp == 'z')
      calibration_factor -= 0.1;
    else if (temp == 's')
      calibration_factor += 10;
    else if (temp == 'x')
      calibration_factor -= 10;
    else if (temp == 'd')
      calibration_factor += 100;
    else if (temp == 'c')
      calibration_factor -= 100;
    else if (temp == 'f')
      calibration_factor += 1000;
    else if (temp == 'v')
      calibration_factor -= 1000;
    else if (temp == 't')
      scale.tare();
  }
}

int cek_berat() {
  scale.set_scale(final_kalibrasi);
  GRAM = scale.get_units(), 4;
  //  Serial.println(GRAM);
  return GRAM;
}
