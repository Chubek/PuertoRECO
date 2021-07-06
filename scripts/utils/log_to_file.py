from dotenv import dotenv_values
import datetime
import os
import getpass
import re

temp = dotenv_values(".env")

log_file = None

def open_log_file(session_type="test"):
    global log_file
    ss_strp = re.sub(r"\s+", " ", session_type.strip())
    date = datetime.datetime.now()
    date_str = date.strftime("%b %d %Y %H:%M:%S")
    sstype = " ".join([s.capitalize() for s in ss_strp.split(" ")])
    log_file = open(temp['LOG_LOC'], 'a' if os.path.exists(temp['LOG_LOC']) else 'w')
    print(f"<----- {sstype} session opened at {date_str} by {getpass.getuser()} ----->\n")
    log_file.write(f"<----- {sstype} session opened at {date_str} by {getpass.getuser()} ----->\n")

def log_to_file(message, type_message="INFO"):
    message_strp = re.sub(r"\s+", " ", message.strip().strip(r'\n'))

    print(f"{type_message} --- {message_strp}")
    global log_file
    date = datetime.datetime.now()
    date_str = date.strftime("%b %d %Y %H:%M:%S")

    log_file.write(f"{type_message} --- {date_str} --- {message_strp}\n")

def close_log_file():
    global log_file
    date = datetime.datetime.now()
    date_str = date.strftime("%b %d %Y %H:%M:%S")
    print(f"<----- Session closed at {date_str} by {getpass.getuser()} ----->\n")
    log_file.write(f"<----- Session closed at {date_str} by {getpass.getuser()} ----->\n\n\n")
    log_file.close()