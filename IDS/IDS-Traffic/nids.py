# PYTHON SCRIPT TO PERFORM ATTACK ANALYSIS

import warnings
import time
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

warnings.filterwarnings(action="ignore")
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
from threading import Thread
from data.modules import constants as cs

""" INTERNAL VARIABLES """
# Store all the module threads and check for crashes
module_pool = []

# Thread name mapping with module
module_mapping = {}
LOG_HEAD = "[MAIN MODULE]: "

if cs.NIDS_ANALYSER_MODULE:
    from data.modules import nids_cic_analyser

    module_mapping["NIDS Analyser Module"] = nids_cic_analyser

if cs.NIDS_SNIFF_MODULE:
    from data.modules import nids_cic_sniff

    module_mapping["NIDS Sniffing Module"] = nids_cic_sniff

if cs.UBIDOT_UPLOAD_MODULE:
    from data.modules import ubidot_handler

    module_mapping["Ubidot Module"] = ubidot_handler

def module_nids_analyser():
    if cs.NIDS_ANALYSER_MODULE:  # If module is enabled, start the module in thread

        print(LOG_HEAD + "*** MODULE NIDS ANALYSER LOADED *** ")
        thread = Thread(target=nids_cic_analyser.start, name="NIDS Analyser Module")
        thread.start()
        module_pool.append(thread)


def module_nids_sniffing():
    if cs.NIDS_SNIFF_MODULE:  # If module is enabled, start the module in thread
        print(LOG_HEAD + "*** MODULE NIDS Sniffing LOADED *** ")
        thread = Thread(target=nids_cic_sniff.start, name="NIDS Sniffing Module")
        thread.start()
        module_pool.append(thread)


def module_ubidot():
    if cs.UBIDOT_UPLOAD_MODULE:  # If module is enabled, start the module in thread
        print(LOG_HEAD + "*** UBIDOT MODULE LOADED *** ")
        thread = Thread(target=ubidot_handler.start, name="Ubidot Module")
        thread.start()
        module_pool.append(thread)


# ************** STARTUP POINT ****************#
print("\n" + LOG_HEAD + "Starting the NIDS modules")

module_nids_analyser()
module_nids_sniffing()
module_ubidot()

while True:
    try:
        status = ""
        for x in module_pool:
            # Check module status
            status += (
                "\n\t" + x.name + ": " + ("Running" if x.is_alive() else "Stopped")
            )

        print("\n" + LOG_HEAD + "Module Status - {}".format(status))
        for x in module_pool:
            if not x.is_alive():
                # If any module is stopped or crashed, start it again (Recovery Mode)
                print(LOG_HEAD + "Restarting " + x.name + " module...")
                thread = Thread(target=module_mapping[x.name].start, name=x.name)
                thread.start()
                module_pool.remove(x)
                module_pool.append(thread)
                break

    except Exception as ex:
        print(LOG_HEAD + "EXCEPTION: " + str(ex))
    finally:
        time.sleep(3)
