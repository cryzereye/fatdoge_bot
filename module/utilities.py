from datetime import datetime
import os

if not os.path.exists('logs'):
    os.makedirs('logs')

def logger(message):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y")
    ts_string = now.strftime("%d/%m/%Y %H:%M:%S")

    if os.path.exists("logs/log_" + dt_string + ".log"):
        f = open("logs/log_" + dt_string + ".log", "a")
    else:
        f = open("logs/log_" + dt_string + ".log", "x")
    f.write(ts_string + "  ---  " + message + "\n")
    f.close()