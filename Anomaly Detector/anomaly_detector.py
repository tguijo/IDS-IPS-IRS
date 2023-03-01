import pandas as pd
import numpy as np
import numpy
from numpy import array
import paho.mqtt.client as mqtt #import the mqtt client
import time
import os, os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import math
import random
from matplotlib import pyplot as plt
from pathlib import Path
import tensorflow
from tensorflow import keras
from tensorflow.keras.layers import Conv1D, Dense, Flatten, MaxPooling1D
from tensorflow.keras.models import Model, load_model
tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)

print("\nLoading saved models....\n")
humedad1_model     = load_model('anomalyModel.h5')
humedad2_model     = load_model('anomalyModel.h5')
temperatura1_model = load_model('anomalyModel.h5')
temperatura2_model = load_model('anomalyModel.h5')
presion1_model     = load_model('anomalyModel.h5')
presion2_model     = load_model('anomalyModel.h5')
humedad1_model.summary() #printing summary of only one for sample

print("\nLoading saved weights in respective models....\n")

humedad1_model.load_weights('./saved_weights/humedad1_weights')
humedad2_model.load_weights('./saved_weights/humedad2_weights')
temperatura1_model.load_weights('./saved_weights/temperatura1_weights')
temperatura2_model.load_weights('./saved_weights/temperatura2_weights')
presion1_model.load_weights('./saved_weights/presion1_weights')
presion2_model.load_weights('./saved_weights/presion2_weights')

print("\nModels and weights loaded....\n")



def current_predicted(x_input_name,model):
    steps = 3
    features = 1
    x_input = np.array(df[x_input_name].iloc[-4:], dtype=float)
    current_received = x_input[3]
    x_input = x_input[0:3]
    x_input = x_input.reshape((1, steps, features))
    y_pred = model.predict(x_input, verbose=0)
    print("**************************************************************")
    print("Current value predicted according to previous values")
    print(f"The predicted value for the sequence {x_input_name}  {x_input} is\n")
    print(y_pred)
    print("and Received value is {}".format(current_received))
    print("**************************************************************")

def predict(x_input_name,model):
    steps = 3
    features = 1
    x_input = np.array(df[x_input_name].iloc[-3:], dtype=float)
    x_input = x_input.reshape((1, steps, features))
    y_pred = model.predict(x_input, verbose=0)
    print("**************************************************************")
    print(f"The next predicted value for the sequence {x_input_name} {x_input} is\n")
    print(y_pred)
    print("**************************************************************")

def sendMail(sensor_name):
    mail_content = "An anomaly has been detected in the reception of data from the sensor #{sensor_name}#, Please check it."
    mail_content = mail_content.format(sensor_name = sensor_name)
    #The mail addresses and password
    sender_address = 'idsiotcm2022@gmail.com'
    sender_pass = 'uukslxikrlnrnmju'
    receiver_address = 'cdavidf98@gmail.com'
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Anomaly detected.'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    print('Signing in to Gmail')
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    print('Sending Gmail')
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')




newMessage     =  False

humedad_1      =  0
temperatura_1  =  0
presion_1      =  0
humedad_2      =  0
temperatura_2  =  0
presion_2      =  0

broker_address =  "localhost"

anomal_sensor  =  ""

sensores       =  "Humedad 1,Temperatura 1,Presion 1,Humedad 2,Temperatura 2,Presion 2"



TOKEN          = "BBFF-uAszWik62GKJzIk26TON8sdVaWa8uv"  # Ubidots TOKEN
DEVICE_LABEL   = "Anomaly-Detector"  # Ubidots device label


def build_payload():
    global humedad_1, temperatura_1, presion_1, humedad_2, temperatura_2, presion_2
    payload = {"humedad-1"      : humedad_1,
               "humedad-2"      : humedad_2,
               "presion-1"      : presion_1,
               "presion-2"      : presion_2,
               "temperatura-1"  : temperatura_1,
               "temperatura-2"  : temperatura_2}

    return payload


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
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def on_message(client, userdata, message):
    global newMessage, humedad_1, temperatura_1, presion_1, humedad_2, temperatura_2, presion_2
    if(message.topic == "datos1"):
        datos1_array = x = str(message.payload.decode("utf-8")).split(",")
        humedad_1 = int(datos1_array[0])
        temperatura_1 = int(datos1_array[1])
        presion_1 = int(datos1_array[2])
    elif (message.topic == "datos2"):
        datos2_array = x = str(message.payload.decode("utf-8")).split(",")
        humedad_2 = int(datos2_array[0])
        temperatura_2 = int(datos2_array[1])
        presion_2 = int(datos2_array[2])
    newMessage = True



def plot_and_save_plots(df):
    global fig, ax1, ax2, ax3, ax4, ax5, ax6
    noOfRecords = -1500
    plt.pause(0.001)

    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    ax5.grid()
    ax6.grid()

    ax1.plot(df['Humedad 1'].iloc[noOfRecords:])
    ax1.set_title('Humedad 1')
    ax2.plot(df['Temperatura 1'].iloc[noOfRecords:])
    ax2.set_title('Temperatura 1')
    ax3.plot(df['Presion 1'].iloc[noOfRecords:])
    ax3.set_title('Presion 1')
    ax4.plot(df['Humedad 2'].iloc[noOfRecords:])
    ax4.set_title('Humedad 2')
    ax5.plot(df['Temperatura 2'].iloc[noOfRecords:])
    ax5.set_title('Temperatura 2')
    ax6.plot(df['Presion 2'].iloc[noOfRecords:])
    ax6.set_title('Presion 2')
    plt.subplots_adjust(left=0.1,
                        bottom=0.1, 
                        right=0.9, 
                        top=0.9, 
                        wspace=0.6, 
                        hspace=0.6)
    Path("./saved_figures").mkdir(parents=True, exist_ok=True)
    #noOfPreviousFiles = len([name for name in os.listdir('./saved_figures') if os.path.isfile(name)])
    noOfPreviousFiles = len(os.listdir('./saved_figures'))
    print(noOfPreviousFiles)
    prefix = "{:04d}".format(noOfPreviousFiles+1)
    print(prefix)
    plt.savefig('./saved_figures/anomaly_'+prefix+'.png')
    plt.show()
    #plt.close('all')


#Below lines reads 'sample.csv' file and stores the data
df = pd.read_csv('sample.csv')

humedad1_historia     = set(df['Humedad 1'].unique())
humedad2_historia     = set(df['Humedad 2'].unique())
temperatura1_historia = set(df['Temperatura 1'].unique())
temperatura2_historia = set(df['Temperatura 2'].unique())
presion1_historia     = set(df['Presion 1'].unique())
presion2_historia     = set(df['Presion 2'].unique())
#End of reading 'sample.csv' file and stores the data

fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=6, sharex=True)
plt.ion()
plot_and_save_plots(df)
plot_and_save_plots(df)




print("creating new instance")
client = mqtt.Client("RaspberryPi4") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topics", "datos1, datos2")
client.subscribe("datos1")
client.subscribe("datos2")

while (1):
    if(newMessage):
        print ("\n")
        print ("Humedad 1     : ", humedad_1)
        print ("Humedad 2     : ", humedad_2)
        print ("Temperatura 1 : ", temperatura_1)
        print ("Temperatura 2 : ", temperatura_2)
        print ("Presion 1     : ", presion_1)
        print ("Presion 2     : ", presion_2)
        data_row = {"Humedad 1"      : humedad_1,
                    "Humedad 2"      : humedad_2,
                    "Presion 1"      : presion_1,
                    "Presion 2"      : presion_2,
                    "Temperatura 1"  : temperatura_1,
                    "Temperatura 2"  : temperatura_2}
        #concating new data to old data
        df = pd.concat([df, pd.DataFrame.from_records([data_row])], ignore_index=True)
        #Concerning increasing size of df, limiting the data to last 3,500 entries
        df = df.tail(3500)
        plot_and_save_plots(df)
        newMessage = False
        if((int(humedad_1) in humedad1_historia) and 
           (int(humedad_2) in humedad2_historia) and 
           (int(temperatura_1) in temperatura1_historia) and 
           (int(temperatura_2) in temperatura2_historia) and 
           (int(presion_1) in presion1_historia) and 
           (int(presion_2) in presion2_historia) ):
            print("\nSensor Values are Normal")
        else:
            if(not(int(humedad_1) in humedad1_historia)):
                anomal_sensor = "Humedad 1"
            elif(not(int(humedad_2) in humedad2_historia)):
                anomal_sensor = "Humedad 2"
            elif(not(int(temperatura_1) in temperatura1_historia)):
                anomal_sensor = "Temperatura 1"
            elif(not(int(temperatura_2) in temperatura2_historia)):
                anomal_sensor = "Temperatura 2"
            elif(not(int(presion_1) in presion1_historia)):
                anomal_sensor = "Presion 1"
            elif(not(int(presion_2) in presion2_historia)):
                anomal_sensor = "Presion 1"
                
            print("\nAn anomaly has been detected in {sensor_name}".format(sensor_name = anomal_sensor))

            sendMail(anomal_sensor)
        payload = build_payload()
        print("[INFO] Attemping to send data to Ubidots")
        post_request(payload)
        print("[INFO]Sending data to Ubidots finished successfully!")
        current_predicted('Humedad 1',humedad1_model)
        predict('Humedad 1',humedad1_model)
        current_predicted('Humedad 2',humedad2_model)
        predict('Humedad 2',humedad2_model)
        current_predicted('Temperatura 1',temperatura1_model)
        predict('Temperatura 1',temperatura1_model)
        current_predicted('Temperatura 2',temperatura2_model)
        predict('Temperatura 2',temperatura2_model)
        current_predicted('Presion 1',presion1_model)
        predict('Presion 1',presion1_model)
        current_predicted('Presion 2',presion2_model)
        predict('Presion 2',presion2_model)
    time.sleep(0.2)
    pass
