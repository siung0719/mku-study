#include <Servo.h>

Servo t;
Servo p;

String cmd;
String pan;
String til;

float s1;
float s2;

float pm = 90;
float tm = 90;

float p_val;
float t_val;

long map(long x, long in_min, long in_max, long out_min, long out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  p.attach(11);
  t.attach(10);
  t.write(94);
  p.write(90);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    cmd = Serial.readString();
    int f = cmd.indexOf(" ");
    int l = cmd.indexOf("\n");
    if (cmd.substring(0,1) == "p") {
      s1 = cmd.substring(1, f).toFloat();
      s2 = cmd.substring(f + 1, l).toFloat();
      pm = pm + s1;
      tm = tm + s2;
      if (pm > 140) {
        pm = 140;
      } else if (pm < 40) {
        pm = 40;
      }
      if (tm > 180) {
        tm = 180;
      } else if (tm < 70) {
        tm = 70;
      }

      p.write(pm);
      t.write(tm);
    }
  }
}
