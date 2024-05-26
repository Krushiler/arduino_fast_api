#include "Config.h"
#include "WIFI.h"
#include "Server.h"
#include "leds.h"
#include "MQTT.h"


void setup(void){
  Serial.begin(115200);
  pinMode(led, OUTPUT);
  for(int i=0; i< 3; i++) { 
    digitalWrite(led, !digitalRead(led));
    delay(500);
  }
  leds_init();
  WIFI_init(false);
  server_init();
  // set_leds_bytes("0000003400000049000000640000007900000094000000109000000124000000139000000154000000169000000184000000199000000214000000229000000244", 15);
  MQTT_init();
  mqtt_cli.publish(("lab/krushiler/strip/" + WiFi.macAddress()).c_str(), "hello emqx");
  mqtt_cli.subscribe(("lab/krushiler/strip/" + WiFi.macAddress() + "/set_leds").c_str());
  mqtt_cli.subscribe(("lab/krushiler/strip/" + WiFi.macAddress() + "/set_leds_bytes").c_str());
  // mqtt_cli.subscribe("lab/krushiler/strip/" + WiFi.macAddress() + "/rotate_leds");
  // mqtt_cli.subscribe("lab/krushiler/range/");
  
  Serial.println(WiFi.macAddress());
}

void loop(void){
  server.handleClient();                   
  mqtt_cli.loop();
}