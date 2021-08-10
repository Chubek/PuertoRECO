import mysql.connector
from scripts.utils.log_to_file import log_to_file
from scripts.utils.validate_env import validate_mysql_env
import os
import inspect


db_client = None
COMMAND_INSERT = None
COMMAND_UPDATE_NAME = None
COMMAND_UPDATE_PATH = None
COMMAND_SELECT = None

    

sql_uri, code, not_in_env, env_errs = validate_mysql_env(os.getcwd())

if code == 176:
    log_to_file("Problem with MySQL URI. Aborting...", "ERROR")

try:
    log_to_file("Creating MySQL client...", "INFO")
    db_client = mysql.connector.connect(
            host=sql_uri['URI'],
            user=sql_uri['USER'],
            password=sql_uri['PASS'],
            database=sql_uri['SCHEMA']
    )
    COMMAND_INSERT = f"INSERT INTO {sql_uri['TABLE']} ({sql_uri['ID_COL']}, {sql_uri['NAME_COL']}, {sql_uri['PATH_COL']}) VALUES (%s, %s, %s)"
    COMMAND_UPDATE_PATH = f"UPDATE {sql_uri['TABLE']} SET {sql_uri['PATH_COL']} = %s WHERE {sql_uri['ID_COL']} = %s"
    COMMAND_UPDATE_NAME = f"UPDATE {sql_uri['TABLE']} SET {sql_uri['NAME_COL']} = %s WHERE {sql_uri['ID_COL']} = %s"
    COMMAND_SELECT = lambda id_: f"SELECT * from {sql_uri['TABLE']} WHERE {sql_uri['ID_COL']} = '{id_}'"


    log_to_file("Created MySQL client successfully.", "SUCCESS")
except:
    log_to_file("Error creating MySQL client, check SQL_URI.", "ERROR")


def insert_to_db(id_, name, db_path, in_place_id=False):
    global db_client
    try:
        cursor = db_client.cursor()
    except:
        db_client = mysql.connector.connect(
            host=sql_uri['URI'],
            user=sql_uri['USER'],
            password=sql_uri['PASS'],
            database=sql_uri['SCHEMA']
        )
        cursor = db_client.cursor()

    if in_place_id == 850 or (in_place_id != 800 and in_place_id != 838):
        cursor.execute(COMMAND_UPDATE_NAME, (name, id_))
        cursor.execute(COMMAND_UPDATE_PATH, (db_path, id_))
        db_client.commit()

        message = 850 if in_place_id == 850 else 900

        log_to_file(f'ID {id_} already exists in db. Folder deleted and DB path replaced or updated.', "INFO")
        return in_place_id, message
    else:
        log_to_file(f'ID {id_} does not exist in MySQL. Inserting...', "INFO")
        cursor.execute(COMMAND_INSERT, (id_, name, db_path))
        db_client.commit()
    
    in_place_log = {
        838: "in_place was needlessly enabled.",
        850: "in_place was disalbed so files were added.",
        800: "in_place was disalbed and ID wasn't in DB, original data was created."
    }

    log_to_file(f'{in_place_log[in_place_id]}', "SUCCESS")
    return cursor.lastrowid, in_place_id

def select_from_db(id_):
    log_to_file(f"Selecting from DB given ID {id_}", "INFO")
    global db_client
    try:
        cursor = db_client.cursor()
    except:
        db_client = mysql.connector.connect(
            host=sql_uri['URI'],
            user=sql_uri['USER'],
            password=sql_uri['PASS'],
            database=sql_uri['SCHEMA']
        )
        cursor = db_client.cursor()

    cursor.execute(COMMAND_SELECT(id_))

    
    res_all = cursor.fetchall()

    log_to_file(f"ID selected from DB. Got results {res_all}", "INFO")

    if len(res_all) == 0:
        res = []
    else:
        res = res_all[0]

    return res

