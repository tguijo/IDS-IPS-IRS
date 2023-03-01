#include <OneWire.h>       //libreria temperatura digital
#include <DallasTemperature.h> //libreria temperatura digital
#include <Adafruit_BMP085.h> //libreria barometrico y temperatura digital
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_ADS1015.h>

OneWire ourWire(17);                //Se establece el pin 4  como bus OneWire temperatura digital
DallasTemperature sensors(&ourWire); //Se declara una variable u objeto para nuestro sensor temperatura
Adafruit_BMP085 bmp;

//inicializamos objeto client
WiFiClient espClient;
PubSubClient client(espClient);

//servidor de internet
const char* ssid = "Lab. Telematica";
const char* password = "l4bt3l3m4tic@";
const char* mqtt_server = "192.168.10.111";

//creamos objeto clase adafruit
Adafruit_ADS1115 ads;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password); //se conecta al wifi
  while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
  ads.begin();
  bmp.begin();
  sensors.begin(); //sensor temperatura ambiente

  client.setServer(mqtt_server, 1883); //defino el servidor mqtt
  client.connect("arduinoClient");
  //delay(5000);
}

void loop() {
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

//   humedad tierra
   short adc0 = ads.readADC_SingleEnded(0);
   int humedad = map(adc0, 32767, 1, 0, 100);
  
  //temperatura digital 
  sensors.requestTemperatures();   //Se envía el comando para leer la temperatura
  int tempSuelo= sensors.getTempCByIndex(0); //Se obtiene la temperatura en ºC
 
  //barometrico
  //SCL-G22, SDA-G21
  long presion = bmp.readPressure();
 
  //creacion de la cadena
  String cadena = String(humedad)+","+String(tempSuelo)+","+String(presion);

  Serial.println(cadena);
  delay(2000);
  
  client.setServer(mqtt_server, 1883); //defino el servidor mqtt
  client.connect("arduinoClient");
  client.publish("datos2", cadena.c_str());//envio datos por mqtt
  delay(60000);
 }
