import pathlib

# CONSTANTS File

""" Module Flags """
# These flags control which modules to enable
NIDS_ANALYSER_MODULE = True
NIDS_SNIFF_MODULE = True
UBIDOT_UPLOAD_MODULE = True

""" Feature Flags """
# These flags control which features to enable
EMAIL_ANALYSIS = True
TRUNCATE_NETWORK_DATA = False

""" Variables """
CURRENT_PATH = pathlib.Path(__file__).parent.resolve()

EMAIL_FROM = "idsiotcm2022@gmail.com"
EMAIL_PASSWORD = "kovdxqljgowfmhcm"
EMAIL_TO = "cdavidf98@gmail.com"

UBIDOT_TOKEN = "BBFF-uAszWik62GKJzIk26TON8sdVaWa8uv"
UBIDOT_DEVICE = "IDS-Traffic"

# Network Interface to analyse
CIC_INTERFACE = "wlan0"

# Directories and Files
DATA_DIR = "./data"
MODEL_DIR = DATA_DIR + "/model"
NETWORK_DIR = DATA_DIR + "/network"
CIC_PATH = "/usr/local/bin/cicflowmeter"
NETWORK_MAPPINGS_FILE_NAME = NETWORK_DIR + "/mappings.csv"
NETWORK_ATTACKS_FILE_NAME = NETWORK_DIR + "/attacks.csv"
NETWORK_DATA_FILE_NAME = DATA_DIR + "/networkdata.csv"
IDS_MODEL = MODEL_DIR + "/clf.jbl.lzma"
