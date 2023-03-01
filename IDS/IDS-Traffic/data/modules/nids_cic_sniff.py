# The program to monitor the network interface packets
# This program stores the packets in CSV file

import subprocess
from .constants import *

LOG_HEAD = "[NIDS SNIFFER]: "
def start():
    while True:
        print(LOG_HEAD + "Sniffing packets on interface:" + CIC_INTERFACE)
        process = subprocess.Popen(
            [
                CIC_PATH,
                "-i",
                CIC_INTERFACE,
                "-c",
                str(CURRENT_PATH) + "/../networkdata.csv",
            ]
        )
        process.communicate()
