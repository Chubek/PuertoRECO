from dotenv import dotenv_values
import datetime
import os

temp = dotenv_values(".env")

log_file = open(temp['LOG_LOC'], 'a' if os.path.exists(temp['LOG_LOC']) else 'w')

def log_to_file(message, type):
    date = datetime.datetime.now()
    date_str = date.strftime("%b %d %Y %H:%M:%S")

    log_file.write(f"{type} - {date_str} - {message}")


log_file.close()