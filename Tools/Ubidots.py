import paho.mqtt.client as mqtt #import the client1
import time
import os
import RPi.GPIO as GPIO
import requests
from time import sleep

k1 = 0
k2 = 0
k3 = 0
k4 = 0
k5 = 0
k6 = 0

TOKEN = "BBFF-uAszWik62GKJzIk26TON8sdVaWa8uv" # Put your TOKEN here
DEVICE_LABEL = "anomaly-detector" # Put your device label here
VARIABLE_LABEL_1 = "Humidity 1"
VARIABLE_LABEL_2 = "Temperature 1"
VARIABLE_LABEL_3 = "Pressure 1"
VARIABLE_LABEL_4 = "Humidity 2"
VARIABLE_LABEL_5 = "Temperature 2"
VARIABLE_LABEL_6 = "Pressure 2"
datos1 = ""
datos2 = ""
sensores = "Humidity 1,Temperature 1,Pressure 1,Humidity 2,Temperature 2,Pressure 2"


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

def post_request2(payload2):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload2)
        status = req.status_code
        attempts += 1
        sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True
 
def subir(info):
        payload = {VARIABLE_LABEL_1: info.split(",")[0],
                  VARIABLE_LABEL_2: info.split(",")[1],
                    VARIABLE_LABEL_3: info.split(",")[2]}
        payload2 = {VARIABLE_LABEL_4: info.split(",")[3],
                  VARIABLE_LABEL_5: info.split(",")[4],
                   VARIABLE_LABEL_6: info.split(",")[5]}
        print("[INFO] Attemping to send data")
        post_request(payload)
        post_request2(payload2)
        print("[INFO] finished") 


############
def on_message(client, userdata, message):
    global datos1,datos2
    if(message.topic == "datos1"):
        datos1 = str(message.payload.decode("utf-8"))
    elif (message.topic == "datos2"):
        datos2 = str(message.payload.decode("utf-8"))
    
    ########################################
broker_address="localhost"

print("creating new instance")
client = mqtt.Client("RaspberryPi4") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
#print("Subscribing to topic","house/bulbs/bulb1")

client.subscribe("datos1")
client.subscribe("datos2")
while (1):
    print ("Nodo 1: ", datos1)
    print ("Nodo 2: ", datos2)
    cadena = datos1 + "," + datos2
    #Subir a ubidots
    if (len(cadena)>3):
        subir(cadena)
            
    time.sleep(68)
   
    pass
