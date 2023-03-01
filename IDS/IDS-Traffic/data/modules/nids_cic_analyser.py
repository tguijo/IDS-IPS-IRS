# This file analyses the network packets and checks if there is any attack or not

from .constants import *
import pandas as pd
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import RobustScaler
import time
import smtplib
import threading
import pyautogui as pag
import json
import joblib

LOG_HEAD = "[NIDS ANALYSER]: "

"""
    Load network labels from the file
"""
nmappings = None
attacks_labels = None
network_df = pd.DataFrame()

# Popup message to user


def alertmsg(message):
    pag.alert(message, "NIDS Security")

# Start popup in thread to avoid blocking the main program


def alert_thread(message):
    thread = threading.Thread(target=alertmsg, args=(message,))
    thread.start()

# Load the network label mappings


def load_labels():
    global nmappings, attacks_labels

    print(LOG_HEAD + "Loading the network label mappings data from the file system...")
    nmappings = pd.read_csv(NETWORK_MAPPINGS_FILE_NAME,
                            names=("c1", "c2"))  # Read data
    print(LOG_HEAD + ">>> Loaded the network label mappings successfully.")

# Get the packets from the sniffer via CSV file


def load_network_packets():
    global network_df
    print(
        LOG_HEAD
        + "Loading the network packets data from the network mpnitoring system..."
    )
    try:
        network_df = pd.read_csv(NETWORK_DATA_FILE_NAME)  # Read data
    except pd.errors.EmptyDataError as error:
        print(LOG_HEAD + ">>> No network packets monitored yet for analysis.")
        return

    # Once the data is loaded, truncate the CSV
    if TRUNCATE_NETWORK_DATA:
        try:
            with open(NETWORK_DATA_FILE_NAME, "r+") as f:
                f.truncate()
        except IOError as err:
            print(
                LOG_HEAD
                + ">>> Unable to truncate the network data file. Reason: "
                + str(err)
            )
            print(LOG_HEAD + ">>> I might re-analyse same data in next run.")

    network_df.columns = network_df.columns.str.lstrip()

    # Transform the data set
    network_df.rename(columns=dict(
        zip(nmappings["c2"], nmappings["c1"])), inplace=True)
    nmappings_list = list(nmappings["c1"])
    # for x in network_df.columns:
    #     if x not in nmappings_list:
    #         network_df.drop(x, axis=1, inplace=True)
    print(LOG_HEAD + ">>> Removed the outliers.")

    for x in range(len(nmappings_list)):
        if x < len(network_df.columns):
            network_df.insert(x, nmappings_list[x], network_df.pop(nmappings_list[x]))

    features=["Bwd Packet Length Std", "Flow Bytes/s", "Total Length of Fwd Packets", "Fwd Packet Length Std",
     "Flow IAT Std", "Flow IAT Min", "Fwd IAT Total"]

    # network_df.info()
    network_df = network_df[features]
    network_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    network_df=network_df.fillna(0)
    # print(len(network_df))

    print(LOG_HEAD + ">>> Transformed the metadata successfully.")
    print(LOG_HEAD + ">>> Loaded the network packets data successfully.")


# Predict using the CIC IDS 2017 model
def predict():
    global network_df
    if len(network_df) == 0 or network_df.empty:
        return

    reconstructed_model = joblib.load(IDS_MODEL)

    print(LOG_HEAD + "Initializing the prediction.")
    classes_x = reconstructed_model.predict(network_df)
    classes_x_prba = reconstructed_model.predict_proba(network_df)
    # print(classes_x_prba)
    print(LOG_HEAD + ">>> Prediction process completed.")
    if len(classes_x[classes_x != "BENIGN"]) == 0:
        # No attacks
        print(LOG_HEAD + "No attacks found in the monitored network packets.")
        return
    attacks = {}
    confidence = {}
    for x in range(len(classes_x)):
        if classes_x[x] in confidence:
            confidence[classes_x[x]].append(classes_x_prba[x])
        else:
            confidence[classes_x[x]] = [classes_x_prba[x]]

    unique, counts = np.unique(classes_x, return_counts=True)

    # Collecting analysis
    for i in range(len(unique)):
        attacks[unique[i]] = {
            "Count": int(counts[i]), "Confidence": float("{:.4}".format(np.max(confidence[unique[i]])))}

    print(LOG_HEAD + ">>> Attack Report:",
          json.dumps(attacks, indent=4, sort_keys=True))

    # Email the analysis
    for i in attacks:
        if i == "BENIGN":
            continue
        message = "An intruder has been detected on your network, who is carrying out an attack of the type {}.\nThis attack has a {:.2%} reliability.\nPlease take corrective action".format(
            i, attacks[i]["Confidence"])
        alertmsg(message)

        if EMAIL_ANALYSIS:
            emessage = "Subject: {}\n\n{}".format("Intruder Detected", message)

            s = smtplib.SMTP("smtp.gmail.com", 587)
            s.starttls()
            s.login(EMAIL_FROM, EMAIL_PASSWORD)
            s.sendmail(EMAIL_FROM, EMAIL_TO, emessage)
            s.quit()
            print(LOG_HEAD + ">>> Attack analysis sent to the email.")

    # upload_ubidot(attacks)
    print(LOG_HEAD + ">>> Attack analysis completed.")

# This function is responsible to upload validated sensor data
def upload_ubidot(data:dict):
    if UBIDOT_UPLOAD_MODULE:
        from data.modules import ubidot_handler as ubidot

        if "BENIGN" in data: data.pop("BENIGN")
        ubidot.upload_attack_data(data)

def start():
    while True:
        load_labels()
        load_network_packets()
        predict()
        print(LOG_HEAD + "Sleeping for 30 seconds")
        time.sleep(30)
