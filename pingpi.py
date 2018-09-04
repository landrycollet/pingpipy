""" pingpi - a simple script for Raspberry Pi to show your ISP it SUCKS! """
__author__ = "Landry COLLET"
__copyright__ = "Copyright (C) 2018, Landry COLLET"
__license__ = "Released under the GNU General Public License v3, see https://www.gnu.org/licenses."
__version__ = "1.0.0"


import os
import string
import subprocess
import sys
from time import time
from datetime import datetime

from multiprocessing import Process

import time, threading


def pingAndLog(logFilePath, serverAddress):
    logFile = open(logFilePath, 'a')
    proc = subprocess.Popen(['ping', '-c', '1', serverAddress], stdout=subprocess.PIPE, stderr = subprocess.PIPE)

    status = ""
    # Look for:
    # "1 packets transmitted, 1 received",
    # or "1 packets transmitted, 0 received",
    # or "ping: cannot resolve www.google.com: Unknown host"
    for line in proc.stdout:
        if ("1 received") in line:
            status = "1; Connected"
        elif ("0 received") in line:
            status = "0; Timeout"
    for line in proc.stderr:
        if ("Unknown") in line:
            status = "0; DNS unreachable"
	if ("failure") in line:
            status = "0; DNS unreachable"
    newLine = time.ctime() + "; " + status + "\n"
    print(newLine)
    logFile.write(newLine)
    logFile.close()
    threading.Timer(20, pingAndLog, [logFilePath, serverAddress]).start()


if len(sys.argv) != 3:
    print("Usage:")
    print("python pingpi.py <logFile> <serverAddress>")
    print("Example:")
    print("python pingpi.py logFile.csv www.google.com")
    sys.exit(1)
else:
    logFilePath = sys.argv[1]
    serverAddress = sys.argv[2]
    pingAndLog(logFilePath, serverAddress)
