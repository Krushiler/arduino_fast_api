#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "Krushiler";
const char* password = "password";

WiFiClient wifiClient;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }

  Serial.println("Connected to WiFi");
}

float getAverageTemperature(const String& payload) {
  DynamicJsonDocument doc(1024);
  deserializeJson(doc, payload);

  if (doc.containsKey("temperatures")) {
    float sum = 0;
    int count = 0;
    JsonArray temperatures = doc["temperatures"];
    for (JsonVariant value : temperatures) {
      sum += value.as<float>();
      count++;
    }
    return count > 0 ? sum / count : 0;
  } else {
    Serial.println("Key 'temperatures' not found in received data");
    return 0;
  }
}

void send_post_request(float temperature) {
  HTTPClient http;

  DynamicJsonDocument doc(200);
  doc["temperature"] = temperature;
  doc["location"] = "ru";

  String json;
  serializeJson(doc, json);

  http.begin(wifiClient, "http://172.20.10.10:5000/temperature");
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.POST(json);
  if (httpCode == HTTP_CODE_OK) {
    Serial.println("POST request sent successfully");
  } else {
    Serial.print("Error sending POST request, HTTP code: ");
    Serial.println(httpCode);
  }

  http.end();
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(wifiClient, "http://172.20.10.10:5000/temperature/all?location=ru");
    int httpCode = http.GET();

    if (httpCode == HTTP_CODE_OK) {
      String payload = http.getString();
      Serial.println(payload);

      float averageTemperature = getAverageTemperature(payload);
      send_post_request(averageTemperature);
    } else {
      Serial.print("Error on HTTP request: ");
      Serial.println(http.errorToString(httpCode).c_str());
    }

    http.end();
  }

  delay(5000);
}
