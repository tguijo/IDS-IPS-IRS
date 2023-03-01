import paho.mqtt.client as mqtt #import the client1
import time
import os

datos1 = ""
datos2 = ""
sensores = "Humedad 1,Temperatura 1,Presion 1,Humedad 2,Temperatura 2,Presion 2"
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
print("Subscribing to topic","house/bulbs/bulb1")
client.subscribe("datos1")
client.subscribe("datos2")

while (1):
    print ("Nodo 1: ", datos1)
    print ("Nodo 2: ", datos2)
    cadena = datos1 + "," + datos2
    listaCadena = cadena.split(",")
    if (len(listaCadena)>5):
        archivo = open("data.csv", "a")
        if os.stat('data.csv').st_size == 0:
            archivo.write(sensores + "\n")
        archivo.write(cadena + "\n")
        archivo.close()
    time.sleep(64)
    pass
