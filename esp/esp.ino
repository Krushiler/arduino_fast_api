#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "Krushiler";
const char* password = "password";

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
  StaticJsonDocument<200> doc;
  deserializeJson(doc, payload);

  if (doc.containsKey("temperatures")) {
    float sum = 0;
    int count = 0;
    for (const auto& value : doc["temperatures"].as<JsonArray>()) {
      sum += value.as<float>();
      count++;
    }
    return sum / count;
  } else {
    Serial.println("Key 'temperatures' not found in received data");
    return 0;
  }
}

void send_post_request(float temperature) {
  WiFiClient client;
  HTTPClient http;

  http.begin(client, "http://192.168.48.110:5000/temperature");
  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<200> doc;
  doc["temperature"] = temperature;
  doc["location"] = "home";

  String json;
  serializeJson(doc, json);

  int httpCode = http.POST(json);
  if (httpCode > 0) {
    if (httpCode == HTTP_CODE_OK) {
      Serial.println("POST request sent successfully");
    } else {
      Serial.print("Error sending POST request, HTTP code: ");
      Serial.println(httpCode);
    }
  } else {
    Serial.println("Error: connection failed");
  }

  http.end();
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    WiFiClient client;

    http.begin(client, "http://192.168.48.110:5000/temperature/all?location=home");
    int httpCode = http.GET();

    if (httpCode > 0) {
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
