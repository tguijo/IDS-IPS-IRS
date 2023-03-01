#include <XBee.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085.h>
#include <DHT.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <OneWire.h>       //libreria temperatura digital
#include <DallasTemperature.h> //libreria temperatura digital

#define DHTPIN 27
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

OneWire ourWire(17);                //Se establece el pin 4  como bus OneWire temperatura digital
DallasTemperature sensors(&ourWire); //Se declara una variable u objeto para nuestro sensor temperatura
Adafruit_BMP085 bmp;
XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();

WiFiClient wifiClient;
PubSubClient client(wifiClient);

const char* ssid = "Lab. Telematica";
const char* password = "l4bt3l3m4tic@";
const char* mqtt_server = "192.168.10.111";
const char* token = "BBFF-kIJmPLD7RtIyi8lACcM0UVF60NUz7H";


void setup() {
  Serial.begin(9600);
  xbee.begin(Serial1);
  dht.begin();
  bmp.begin();
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  client.setServer(mqtt_server, 1883);
}

void loop() {
  xbee.readPacket(); 
  if (xbee.getResponse().isAvailable()) {
    if (xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
      xbee.getResponse().getZBRxResponse(rx);
      float humidity = dht.readHumidity();
      float temperature = dht.readTemperature();
      float pressure = bmp.readPressure() / 100.0F;
      
      String topic = String("/v1.6/devices/nombre_dispositivo");
      String payload = String("{");
      payload += String("\"humedad\":") + String(humidity) + String(",");
      payload += String("\"temperatura\":") + String(temperature) + String(",");
      payload += String("\"presion\":") + String(pressure);
      payload += String("}");

      if (client.connect("arduinoClient", token, "")) {
        Serial.println("Sending data to Ubidots...");
        client.publish(topic.c_str(), payload.c_str());
        client.disconnect();
      } else {
        Serial.println("Unable to connect to Ubidots");
      }
    }
  }
}
