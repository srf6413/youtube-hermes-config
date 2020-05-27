"""This module creates a logger that can be used by any module to log information
for the user. A new logger is created each time the program is run using a timestamp
to ensure a unique name.
"""
import logging
from datetime import datetime
logger = logging.getLogger()
logger.setLevel(logging.INFO)
TIMESTAMP = str(datetime.now().strftime("%Y-%m-%d:%H:%M"))
FILE_TITLE = "logs/" + "log-" + TIMESTAMP + ".log"
output_file_handler = logging.FileHandler(FILE_TITLE)
logger.addHandler(output_file_handler)
