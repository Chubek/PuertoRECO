from genericpath import exists
import os
import re
from dotenv import dotenv_values
from scripts.utils.log_to_file import log_to_file
from pathlib import Path


regex_mysql = re.compile(r"^[A-Za-z\_]+$")
regex_password = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})")
list_models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
regex_models = re.compile(r"[A-Z][a-z]+|([A-Z][a-z]+[A-Z][a-z]+)|([A-Z]+\-[A-Z][a-z]+)|(\,)|([A-Z]+)|(\s)")
regex_url = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def validate_env(script_root):
    log_to_file("Validating .env file...", "INFO")

    
    env_file = os.path.join(script_root, ".env")

    if not os.path.exists(env_file):
        log_to_file(f"ENV file {env_file} does not exist. Aborting...", "ERROR")
        return False, ["Error reading .env: file doesn't exist."], ["Error reading .env: file doesn't exist."]

    temp = dotenv_values(".env")

    env_errs = []
    not_in_env = []


    if 'DB_PATH' in temp:
        if temp['DB_PATH'] == "":    
            log_to_file("Env file configured incorrectly: DB_PATH not set or is not a directory.", "ERROR")
            env_errs.append("Env file configured incorrectly: DB_PATH not set or is not a directory.")
    else:
        log_to_file("DB_PATH is not in .env", "ERROR")
        not_in_env.append("DB_PATH")

    if 'MODEL_PATH' in temp:
        if temp['MODEL_PATH'] == "":
            log_to_file("Env file configured incorrectly: MODEL_PATH not set or is not a directory.", "ERROR")
            env_errs.append("Env file configured incorrectly: MODEL_PATH not set or is not a directory.")
    else:
        log_to_file("MODEL_PATH is not in .env", "ERROR")
        not_in_env.append("MODEL_PATH")

    if 'MODEL_NAME' in temp:
        if temp['MODEL_NAME'] == "" or not re.match(r"([\w\W\w]+).h5", temp['MODEL_NAME']):
            log_to_file("Env file configured incorrectly: MODEL_NAME not set or does not match pattern.", "ERROR")
            env_errs.append("Env file configured incorrectly: MODEL_NAME not set or does not match pattern.")
    else:
        log_to_file("MODEL_NAME is not in .env", "ERROR")
        not_in_env.append("MODEL_NAME")
    
    if 'SELECTED_MODELS' in temp:
        if temp['SELECTED_MODELS'] == "" or not re.match(regex_models, temp['SELECTED_MODELS']):
            log_to_file("Env file configured incorrectly: PSELECTED_MODELS is either empty, or doesn't match the necessary pattern.", "ERROR")
            env_errs.append("Env file configured incorrectly: SELECTED_MODELS is either empty, or doesn't match the necessary pattern.")

    else:
        log_to_file("SELECTED_MODELS is not in .env", "ERROR")
        not_in_env.append("SELECTED_MODELS")           
   

        
    if 'MODEL_URL' in temp:
        if temp['MODEL_URL'] == '' or not re.match(regex_url, temp['MODEL_URL']):
            log_to_file("Env file configured incorrectly: MODEL_URL is either empty or is not a valid URL.", "ERROR")
            env_errs.append("Env file configured incorrectly: MODEL_URL is either empty or is not a valid URL.")
    else:
        log_to_file("MODEL_URL is not in .env", "ERROR")
        not_in_env.append("MODEL_URL")

    if 'TARGET_WIDTH' in temp:
        if temp['TARGET_WIDTH'] == '' or not temp['TARGET_WIDTH'].isnumeric():
            log_to_file("Env file configured incorrectly: TARGET_WIDTH is either empty or not numeric.", "ERROR")
            env_errs.append("Env file configured incorrectly: TARGET_WIDTH is either empty or not numeric.")
    else:
        log_to_file("TARGET_WIDTH is not in .env", "ERROR")
        not_in_env.append("TARGET_WIDTH")

    if 'TARGET_HEIGHT' in temp:        
        if temp['TARGET_HEIGHT'] == '' or not temp['TARGET_HEIGHT'].isnumeric():
            log_to_file("Env file configured incorrectly: TARGET_HEIGHT is either empty or not numeric.", "ERROR")
            env_errs.append("Env file configured incorrectly: TARGET_HEIGHT is either empty or not numeric.")
    else:
        log_to_file("TARGET_HEIGHT is not in .env", "ERROR")
        not_in_env.append("TARGET_HEIGHT")

    if 'NUM_AUG' in temp:
        if temp['NUM_AUG'] == '' or not temp['NUM_AUG'].isnumeric():
            log_to_file("Env file configured incorrectly: NUM_AUG is either empty or not numeric.", "ERROR")
            env_errs.append("Env file configured incorrectly: NUM_AUG is either empty or not numeric.")
    else:
        log_to_file("NUM_AUG is not in .env", "ERROR")
        not_in_env.append("NUM_AUG")

    if 'SIM_FUNC' in temp:
        if temp['SIM_FUNC'] == '' or not temp['SIM_FUNC'] in ["cosine", "euclidean", "euclidean_l2"]:
            log_to_file("Env file configured incorrectly: SIM_FUNC is either empty or not approved. Must be in ['cosine', 'euclidean', 'euclidean_l2'].", "ERROR")
            env_errs.append("Env file configured incorrectly: SIM_FUNC is either empty or not approved. Must be in ['cosine', 'euclidean', 'euclidean_l2'].")

    else:
        log_to_file("SIM_FUNC is not in .env", "ERROR")
        not_in_env.append("SIM_FUNC")

    if 'LOG_LOC' in temp:
        if temp['LOG_LOC'] == '':
            log_to_file("Env file configured incorrectly: LOG_LOC is either empty or not a file.", "ERROR")
            env_errs.append("Env file configured incorrectly: LOG_LOC is either empty or not a file.")
    else:
        log_to_file("LOG_LOC is not in .env", "ERROR")
        not_in_env.append("LOG_LOC")
   


    if 'VER_TOL' in temp:
        if temp['VER_TOL'] == '' or not temp['VER_TOL'].isnumeric():
            log_to_file("Env file configured incorrectly: VER_TOL is empty or is not numeric.", "ERROR")
            env_errs.append("Env file configured incorrectly: VER_TOL is empty or is not numeric.")

    else:
        log_to_file("VER_TOL is not in .env", "ERROR")
        not_in_env.append("VER_TOL")

    if 'VER_TOL_AUG' in temp:
        if temp['VER_TOL_AUG'] == '' or not temp['VER_TOL_AUG'].isnumeric():
            log_to_file("Env file configured incorrectly: VER_TOL_AUG is empty or is not numeric.", "ERROR")
            env_errs.append("Env file configured incorrectly: VER_TOL_AUG is empty or is not numeric.")

    else:
        log_to_file("VER_TOL_AUG is not in .env", "ERROR")
        not_in_env.append("VER_TOL_AUG")

    log_to_file(f".env file validated. {len(not_in_env)} keys not found, {len(env_errs)} errors found.", "INFO")

    if len(not_in_env) == 0 and len(env_errs) == 0:
        return temp, 175, True, True

    return False, 176, not_in_env, env_errs

def validate_id_regex(script_root):
    log_to_file("Validating .env file and ID_REGEX...", "INFO")


    if not os.path.exists(os.path.join(script_root, ".env")):
        return False, ["Error reading .env: file doesn't exist."], ["Error reading .env: file doesn't exist."]

    temp = dotenv_values(".env")

    env_errs, not_in_env = [], []
    
    if 'ID_REGEX' in temp:
        if temp['ID_REGEX'] == '':
            log_to_file("Env file configured incorrectly: ID_REGEX is empty.", "ERROR")
            env_errs.append("Env file configured incorrectly: ID_REGEX is empty.")

        try:
            re.compile(rf"{temp['ID_REGEX']}")
        except:
            log_to_file("Env file configured incorrectly: ID_REGEX is not a valid pattern.", "ERROR")
            env_errs.append("Env file configured incorrectly: ID_REGEX is not a valid pattern.")
    else:
        log_to_file("ID_REGEX is not in .env", "ERROR")
        not_in_env.append("ID_REGEX")

    log_to_file(f"ID_REGEX and .env validated. {len(not_in_env)} keys not found, {len(env_errs)} errors found.", "INFO")


    if len(not_in_env) == 0 and len(env_errs) == 0:
        return temp['ID_REGEX'], 175, True, True

    return False, 176, not_in_env, env_errs



    return False, 176, not_in_env, env_errs

def validate_super_pass(script_root):
    log_to_file("Validating .env file and SUPER_PASS...", "INFO")


    env_file = os.path.join(script_root, ".env")

    if not os.path.exists(env_file):
        log_to_file(f"ENV file {env_file} does not exist. Aborting...", "ERROR")
        return False, ["Error reading .env: file doesn't exist."], ["Error reading .env: file doesn't exist."]

    temp = dotenv_values(".env")

    env_errs, not_in_env = [], []
    
    if 'SUPER_PASS' in temp:
        if temp['SUPER_PASS'] == '':
            log_to_file("Env file configured incorrectly: SUPER_PASS is empty.", "ERROR")
            env_errs.append("Env file configured incorrectly: SUPER_PASS is empty.")

        if not re.match(regex_password, temp['SUPER_PASS']):
            log_to_file("Env file configured incorrectly: SUPER_PASS is not secure.", "ERROR")
            env_errs.append("Env file configured incorrectly: SUPER_PASS is not secure.")
    else:
        log_to_file("SUPER_PASS is not in .env", "ERROR")
        not_in_env.append("SUPER_PASS")

    log_to_file(f"SUPER_PASS and .env validated. {len(not_in_env)} keys not found, {len(env_errs)} errors found.", "INFO")


    if len(not_in_env) == 0 and len(env_errs) == 0:
        return temp['SUPER_PASS'], 175, True, True

    return False, 176, not_in_env, env_errs

def validate_mysql_env(script_root):
    log_to_file("Validating .env file and MySQL related keys...", "INFO")

    env_file = os.path.join(script_root, ".env")

    if not os.path.exists(env_file):
        log_to_file(f"ENV file {env_file} does not exist. Aborting...", "ERROR")
        return False, ["Error reading .env: file doesn't exist."], ["Error reading .env: file doesn't exist."]

    temp = dotenv_values(".env")

    env_errs, not_in_env = [], []

    if 'SQL_URI' in temp:
        if temp['SQL_URI'] == '':
            log_to_file("Env file configured incorrectly: SQL_URI is empty.", "ERROR")
            env_errs.append("Env file configured incorrectly: SQL_URI is empty.")
    else:
        log_to_file("SQL_URI is not in .env", "ERROR")
        not_in_env.append("SQL_URI")

    if 'SQL_USER' in temp:
        if temp['SQL_USER'] == '':
            log_to_file("Env file configured incorrectly: SQL_USER is empty.", "ERROR")
            env_errs.append("Env file configured incorrectly: SQL_USER is empty.")
    else:
        log_to_file("SQL_USER is not in .env", "ERROR")
        not_in_env.append("SQL_USER")

    if 'SQL_PASS' in temp:
        if temp['SQL_PASS'] == '':
            log_to_file("Env file configured incorrectly: SQL_PASS is empty.", "ERROR")
            env_errs.append("Env file configured incorrectly: SQL_PASS is empty.")
    else:
        log_to_file("SQL_PASS is not in .env", "ERROR")
        not_in_env.append("SQL_PASS")

        
    if 'SQL_TABLE' in temp:    
        if temp['SQL_TABLE'] == '' or not re.match(regex_mysql, temp['SQL_TABLE']):
            log_to_file("Env file configured incorrectly: SQL_TABLE is either empty or does not match pattern, it can only be letter and underscore.", "ERROR")
            env_errs.append("Env file configured incorrectly: SQL_TABLE is either empty or does not match pattern, it can only be letter and underscore.")
    else:
        log_to_file("SQL_TABLE is not in .env", "ERROR")
        not_in_env.append("SQL_TABLE")

    if 'SQL_SCHEMA' in temp:
        if temp['SQL_SCHEMA'] == '' or not re.match(regex_mysql, temp['SQL_SCHEMA']):
            log_to_file("Env file configured incorrectly: SQL_SCHEMA is either empty or does not match pattern, it can only be letter and underscore.", "ERROR")
            env_errs.append("Env file configured incorrectly: SQL_SCHEMA is either empty or does not match pattern, it can only be letter and underscore.")
    else:
        log_to_file("SQL_SCHEMA is not in .env", "ERROR")
        not_in_env.append("SQL_SCHEMA")

    if 'PATH_COL' in temp:
        if temp['PATH_COL'] == '' or not re.match(regex_mysql, temp['SQL_SCHEMA']):
            log_to_file("Env file configured incorrectly: PATH_COL is either empty or does not match pattern, it can only be letter and underscore.", "ERROR")
            env_errs.append("Env file configured incorrectly: PATH_COL is either empty or does not match pattern, it can only be letter and underscore.")
    else:
        log_to_file("PATH_COL is not in .env", "ERROR")
        not_in_env.append("PATH_COL")

    if 'NAME_COL' in temp:
        if temp['NAME_COL'] == '' or not re.match(regex_mysql, temp['SQL_SCHEMA']):
            log_to_file("Env file configured incorrectly: NAME_COL is either empty or does not match pattern, it can only be letter and underscore.", "ERROR")
            env_errs.append("Env file configured incorrectly: NAME_COL is either empty or does not match pattern, it can only be letter and underscore.")
    else:
        log_to_file("NAME_COL is not in .env", "ERROR")
        not_in_env.append("NAME_COL")

    if 'ID_COL' in temp:
        if temp['ID_COL'] == '' or not re.match(regex_mysql, temp['SQL_SCHEMA']):
            log_to_file("Env file configured incorrectly: ID_COL is either empty or does not match pattern, it can only be letter and underscore.", "ERROR")
            env_errs.append("Env file configured incorrectly: ID_COL is either empty or does not match pattern, it can only be letter and underscore.")
    else:
        log_to_file("ID_COL is not in .env", "ERROR")
        not_in_env.append("ID_COL")

    log_to_file(f"MySQL keys and .env validated. {len(not_in_env)} keys not found, {len(env_errs)} errors found.", "INFO")

    sql_uri = {
        "SCHEMA": temp['SQL_SCHEMA'],
        "URI": temp['SQL_URI'],
        "PASS": temp['SQL_PASS'],
        "USER": temp['SQL_USER'],
        "ID_COL": temp['ID_COL'],
        "PATH_COL": temp['PATH_COL'],
        "NAME_COL": temp['NAME_COL'],
        "TABLE": temp['SQL_TABLE']
    }

    if len(not_in_env) == 0 and len(env_errs) == 0:
        return sql_uri, 175, True, True

    return False, 176, not_in_env, env_errs


def validate_score_tol(script_root):
    log_to_file("Validating .env file and SCORE_TOL...", "INFO")

    env_file = os.path.join(script_root, ".env")

    env_errs, not_in_env = [], []
    
    if not os.path.exists(env_file):
        log_to_file(f"ENV file {env_file} does not exist. Aborting...", "ERROR")
        return False, ["Error reading .env: file doesn't exist."], ["Error reading .env: file doesn't exist."]

    temp = dotenv_values(".env")

    if 'SCORE_TOL' in temp:
        if temp['SCORE_TOL'] == '':
            log_to_file("Env file configured incorrectly: SCORE_TOL is empty.", "ERROR")
            env_errs.append("Env file configured incorrectly: SCORE_TOL is empty.")

        try:
            _ = float(temp['SCORE_TOL'])
        except:
            log_to_file("Env file configured incorrectly: SCORE_TOL is not float.", "ERROR")
            env_errs.append("Env file configured incorrectly: SCORE_TOL is not float.")

    else:
        log_to_file("SCORE_TOL is not in .env", "ERROR")
        not_in_env.append("SCORE_TOL")

    if 'UPLOAD_FOLDER' in temp:
        if temp['UPLOAD_FOLDER'] == '' or not os.path.isdir(temp['UPLOAD_FOLDER']):
            log_to_file("Env file configured incorrectly: UPLOAD_FOLDER is empty string or is not a path.", "ERROR")
            env_errs.append("Env file configured incorrectly: UPLOAD_FOLDER is empty string or is noth a path.")
        
    else:
        log_to_file("UPLOAD_FOLDER is not in .env", "ERROR")
        not_in_env.append("UPLOAD_FOLDER")

    log_to_file(f"MySQL keys and .env validated. {len(not_in_env)} keys not found, {len(env_errs)} errors found.", "INFO")

    
    if len(not_in_env) == 0 and len(env_errs) == 0:
        if not os.path.exists(temp['UPLOAD_FOLDER']):
            os.makedirs(temp['UPLOAD_FOLDER'])
        return {"SCORE_TOL": float(temp['SCORE_TOL']), "UPLOAD_FOLDER": temp['UPLOAD_FOLDER']}, 175, True, True

    return False, 176, not_in_env, env_errs


def validate_video_temp(script_root):
    log_to_file("Validating .env file and VIDEO_TEMP_PATH...", "INFO")

    env_file = os.path.join(script_root, ".env")

    env_errs, not_in_env = [], []
    
    if not os.path.exists(env_file):
        log_to_file(f"ENV file {env_file} does not exist. Aborting...", "ERROR")
        return False, ["Error reading .env: file doesn't exist."], ["Error reading .env: file doesn't exist."]

    temp = dotenv_values(".env")


    if 'VIDEO_TEMP_PATH' in temp:
        if temp['VIDEO_TEMP_PATH'] == '' or not os.path.isdir(temp['VIDEO_TEMP_PATH']):
            log_to_file("Env file configured incorrectly: VIDEO_TEMP_PATH is empty string or is not a path.", "ERROR")
            env_errs.append("Env file configured incorrectly: VIDEO_TEMP_PATH is empty string or is noth a path.")
        
    else:
        log_to_file("VIDEO_TEMP_PATH is not in .env", "ERROR")
        not_in_env.append("VIDEO_TEMP_PATH")

    if 'FINAL_VIDEO_PATH' in temp:
        if temp['FINAL_VIDEO_PATH'] == '' or not os.path.isdir(temp['FINAL_VIDEO_PATH']):
            log_to_file("Env file configured incorrectly: FINAL_VIDEO_PATH is empty string or is not a path.", "ERROR")
            env_errs.append("Env file configured incorrectly: FINAL_VIDEO_PATH is empty string or is noth a path.")
        
    else:
        log_to_file("FINAL_VIDEO_PATH is not in .env", "ERROR")
        not_in_env.append("FINAL_VIDEO_PATH")

    if len(not_in_env) == 0 and len(env_errs) == 0:
        if not os.path.exists(temp['VIDEO_TEMP_PATH']):
            os.makedirs(temp['VIDEO_TEMP_PATH'])
        if not os.path.exists(temp['FINAL_VIDEO_PATH']):
            os.makedirs(temp['FINAL_VIDEO_PATH'])
        return (temp['VIDEO_TEMP_PATH'], temp['FINAL_VIDEO_PATH']), 175, True, True

    return False, 176, not_in_env, env_errs