#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>

#ifdef __AVR__
  #include <avr/power.h>
#endif

#define LEDPIN 6
#define NUMPIXELS 20
#define PUMPPIN 4

Adafruit_NeoPixel pixels(NUMPIXELS, LEDPIN, NEO_GRB + NEO_KHZ800);

void setup() {
  // For ATtiny85 with 16 MHz, adjust clock prescale if necessary
  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
    clock_prescale_set(clock_div_1);
  #endif

  pinMode(PUMPPIN, OUTPUT);
  pixels.begin();

  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for the serial port to connect
  }
}

void loop() {
  if (Serial.available() > 0) {
    // Read JSON string until newline
    String jsonString = Serial.readStringUntil('\n');

    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, jsonString);

    StaticJsonDocument<200> response;
    if (error) {
      response["code"] = 400;
      response["error"] = error.c_str();
      serializeJson(response, Serial);
      Serial.println();
      return;
    }

    int val = doc["val"];
    const char* cmd = doc["cmd"];

    if (strcmp(cmd, "echo") == 0) {
      response["code"] = 200;
      response["val"] = val;
    }
    else if (strcmp(cmd, "led") == 0) {
      if (val == 1) {
        // Turn on LED: set each pixel to a purple colour (143, 0, 255)
        for (int i = 0; i < NUMPIXELS; i++) {
          pixels.setPixelColor(i, pixels.Color(143, 0, 255));
        }
      }
      else {
        // Turn off LED
        pixels.clear();
      }
      pixels.show();
      response["code"] = 200;
    }
    else if (strcmp(cmd, "pump") == 0) {
      int state = (val == 0) ? LOW : HIGH;
      digitalWrite(PUMPPIN, state);
      response["code"] = 200;
    }
    else if (strcmp(cmd, "both") == 0) {
      if (val == 1) {
        for (int i = 0; i < NUMPIXELS; i++) {
          pixels.setPixelColor(i, pixels.Color(143, 0, 255));
        }
        digitalWrite(PUMPPIN, HIGH);
      }
      else {
        pixels.clear();
        digitalWrite(PUMPPIN, LOW);
      }
      pixels.show();
      response["code"] = 200;
    }
    else {
      response["code"] = 404;
      response["error"] = "Unknown command";
    }

    // Return only the JSON response over Serial
    serializeJson(response, Serial);
    Serial.println();
  }
}