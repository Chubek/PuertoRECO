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

def connect_to_db():
    global db_client
    global COMMAND_INSERT
    global COMMAND_UPDATE_NAME
    global COMMAND_UPDATE_PATH
    global COMMAND_SELECT

    sql_uri, code, not_in_env, env_errs = validate_mysql_env(os.getcwd())

    if code == 176:
        log_to_file("Problem with MySQL URI. Aborting...", "ERROR")
        return code, not_in_env, env_errs

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
        return 129, not_in_env, env_errs
    return 130, None, None

def insert_to_db(id_, name, db_path):
    cursor = db_client.cursor()
    
    try:
        cursor.execute(COMMAND_UPDATE_NAME, (name, id_))
        cursor.execute(COMMAND_UPDATE_PATH, (db_path, id_))
        db_client.commit()
        log_to_file(f'ID {id_} already exists in db. Info updated.', "INFO")
        return "Not Created", 900
    except:
        cursor.execute(COMMAND_INSERT, (id_, name, db_path))
        db_client.commit()
    
 

    log_to_file(f'ID {id} successfully inserted to db. The resulting MySQL identifier is {cursor.lastrowid}', "SUCCESS")
    return cursor.lastrowid, 800

def select_from_db(id_):
    cursor = db_client.cursor()

    cursor.execute(COMMAND_SELECT(id_))

    return cursor.fetchall()[0][1:]

