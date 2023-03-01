# This module communicates with Ubidot and upload the validated data
import time
import requests
from .constants import *
import numpy

Headers = {"X-Auth-Token": UBIDOT_TOKEN, "Content-Type": "application/json"}

LOG_HEAD = "[UBIDOT MODULE]: "

selected_device = ""

# Get the devices list from the Ubidot


def get_devices():
    global selected_device
    print(LOG_HEAD + "Loading devices and variables...")

    url = "https://stem.ubidots.com/api/v2.0/devices"
    response = requests.get(url, headers=Headers)

    if response.status_code // 100 != 2:
        print(LOG_HEAD + "Failed to get devices from Ubidot." + response.text)
        return

    selected_device = UBIDOT_DEVICE
    if response.json()["count"] == 0:
        print(LOG_HEAD + "Found 0 devices cofigured in Ubidot.")
        return

    print(LOG_HEAD + ">>> Loaded devices")

def upload_attack_data(data):
    global selected_device
    while selected_device == "":  # Wait until all the devices are loaded
        time.sleep(5)
        continue

    url = "https://industrial.api.ubidots.com/api/v1.6/devices/{}"

    # Format the upload data
    fulldata = {}
    for attack in data.keys():
        request = []
        unix_secs = int(time.time())*1000
        request.append({"value": float("{:.2}".format(
            data[attack]["Confidence"]*100)), "timestamp": unix_secs})
        fulldata[attack] = request

    # Upload attack data
    response = requests.post(
        url.format(selected_device),
        json=fulldata,
        headers=Headers,
    )
    if response.status_code // 100 != 2:
        print(
            LOG_HEAD
            + "Failed to post attack data to Ubidot device {} - {}".format(
                selected_device, response.text
            )
        )
    else:
        print(
            LOG_HEAD
            + "Uploaded the attack data to the device: "
            + selected_device
            + " successfully"
        )


def start():
    while True:
        if selected_device == "":
            get_devices()
            continue
        time.sleep(24 * 60 * 60)
