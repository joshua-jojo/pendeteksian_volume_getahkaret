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
float final_kalibrasi = 100.20;
int GRAM;

void setup() {
  Serial.begin(115200);
  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);
  lcd.begin();


  scale.set_scale();
  scale.tare();
  long zero_factor = scale.read_average();
  tampil_lcd("Start...", "",2000);
}


void loop() {
  bool cek_loop = true;
  tampil_lcd("Letakkan", "Getah..",2000);
  while (!Serial.available());
  String data = Serial.readStringUntil('\n');
  float tinggi = float(hcsr());
  float data_panjang = panjang(data) / 10.0 ;
  float data_lebar = lebar(data) / 10.0 ;
  float volume = (data_panjang * data_lebar * tinggi) ;
  float berat = volume * 0.61;
  if (berat > 400) {
    tampil_lcd("Karet", "Terdeteksi..",3000);
    if (cek_berat() < 10) {
      while (cek_loop) {
        tampil_lcd("Timbang", "Getah..",3000);
        if (cek_berat() > 1) {
          tampil_lcd("Tim : " + String(cek_berat()) + " gram", "Cit : " + String(int(berat)) + " gram",4000);
          cek_loop = false;
        }
      }
    }
  }
}
int tampil_lcd(String data1, String data2,int waktu) {
  lcd.setCursor(0, 0);
  lcd.print(data1);
  lcd.setCursor(0, 1);
  lcd.print(data2);
  delay(waktu);
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

  distance = 40 - distance;
  return distance;
}

int kalibrasi_berat() {
  scale.set_scale(calibration_factor);
  GRAM = scale.get_units(), 4;
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
  return GRAM;
}

int cek_berat() {
  scale.set_scale(final_kalibrasi);
  GRAM = scale.get_units(), 4;
  //    Serial.println(GRAM);
  return GRAM;
}
int panjang(String data) {
  int index = data.indexOf(' ');
  String data1 = data.substring(0, index);

  int fix;
  fix = data1.toInt();
  return fix;
}
int lebar(String data) {
  int index = data.indexOf(' ');
  String data2 = data.substring(index + 1, data.length());
  int fix;
  fix = data2.toInt();
  return fix;
}

//kalibrasi

// while (!Serial.available());
//  String data = Serial.readStringUntil('\n');
//  //  float tinggi = float(hcsr());
//  //  float data_panjang = panjang(data)/10.0 ;
//  //  float data_lebar = lebar(data)/10.0 ;
//  //  float volume = (data_panjang * data_lebar * tinggi) / 100.0 ;
//  //  float berat_benda = volume * 562.7;
//  //
//  //  data = String(berat_benda);
//  //  tampil_lcd(String(berat_benda),"");
//
//if (String(data) == "kalibrasi "){
//  tampil_lcd("Melakukan","Kalibrasi Berat");
//  while(1){
//   tampil_lcd("kalibrasi : "+String(kalibrasi_berat()),"");
//    }
//}
