import os
from flask import Flask, request, render_template, send_from_directory, url_for, redirect, jsonify
from numpy import save
from dotenv import dotenv_values
from main import *
import re
temp = dotenv_values(".env")
import glob
import platform
import time
from dotenv import dotenv_values
from codes_dict import CODES_DICT
from scripts.utils.server_shutdown import shutdown_server
from scripts.utils.log_to_file import close_log_file
from flask_cors import CORS, cross_origin
from datetime import datetime
import base64
from scripts.utils.generate_id import generate_random_str


temp = dotenv_values(".env")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
@cross_origin()
def verify():
    if len(request.form) == 0:
        return jsonify({"recognition_code": 107, "recognition_message": CODES_DICT[107], "recognition_results": None, "system_errors": None})

    if len(set(['upload_id', 'skip_verify', 'skip_db_search', 'skip_liveness']).intersection(set(request.form.keys()))) != 4:
        return jsonify({"recognition_code": 109, "recognition_message": CODES_DICT[109], "recognition_results": None, "system_errors": None})

    id_folder = request.form['upload_id']
    id_ = id_folder.split("-")[0]

    skip_verify = True if request.form['skip_verify'].lower() == "true" else False
    skip_db_search = True if request.form['skip_db_search'].lower() == "true" else False
    skip_liveness = True if request.form['skip_liveness'].lower() == "true" else False

    folder_path = os.path.join(os.getcwd(), temp['UPLOAD_FOLDER'], id_folder)
    log_to_file(f"Checking if folder {folder_path} exists, or is uploaded before.")
    if os.path.exists(f"{folder_path}_UPLOADED_TO_DB") or not os.path.exists(folder_path):
        log_to_file(f"Folder {folder_path} does not exist has been uploaded before.", "ERROR")
        return jsonify({"recognition_code": 189, "recognition_message": CODES_DICT[189], "recognition_results": None, "system_errors": None})


    id_re_code, not_in_env, env_errs = main_id_regex(id_)

    if id_re_code != 126:
        return jsonify({"recognition_code": 112, "recognition_message": CODES_DICT[id_re_code], "recognition_results": None,\
              "system_errors": {"not_in_env": not_in_env, "env_errs": env_errs}})

    

    if platform.system == "Windows":
        imgs = glob.glob(folder_path + r"\*.[pj][np]*")
    else: 
        imgs = glob.glob(f"{folder_path}/*.[pj][np]*")


    code, name, distance = main_reco(imgs, id_, skip_liveness=skip_liveness, skip_verify=skip_verify, skip_db_search=skip_db_search)

    if code == 176:
        return jsonify({"recognition_code": code, "recognition_message": CODES_DICT[code], "recognition_results": None,\
             "system_errors": {"not_in_env": name, "env_errs": distance}})

    return jsonify({"recognition_code": code, "recognition_message": CODES_DICT[code], "recognition_results": {"name": name, "distance": distance}, "system_errors": None})


@app.route('/upload_imgs', methods=['POST'])
@cross_origin()
def upload_verify():
    if 'id' not in request.args:
        return jsonify({"upload_results": None, "upload_code": 110, "upload_message": CODES_DICT[110], "system_errors": None})
    id_ = request.args['id']


    id_re_code, not_in_env, env_errs = main_id_regex(id_)

    if id_re_code != 126:
        log_to_file("Aborting...", "FAILURE")
        return jsonify({"upload_results": None, "upload_code": id_re_code, "upload_message": \
            CODES_DICT[id_re_code], "system_errors": {"not_in_env": not_in_env, "env_errs": env_errs}})


    files = request.files

    if len(files) == 0:
        return jsonify({"upload_results": None, "upload_code": 117, "upload_message": \
            CODES_DICT[117], "system_errors": None})

    folder_name = f"{id_}-{str(time.time())[-5:]}"


    scores, saved, rejected, errors,  saved_as = assess_quality_and_save(request.files, folder_name)

    if scores == 176:
        return jsonify({"upload_results": None, "upload_code": 176, "upload_message": \
            CODES_DICT[176], "system_errors": {"not_in_env": saved, "env_errs": rejected}})

    if len(saved) == 0:
        return jsonify({"upload_results": {"folder_name": None, "scores": scores, \
        "saved": saved, "rejected": rejected, "errors": errors, "saved_as": None}, "upload_code": 120, "upload_message": \
            CODES_DICT[120], "system_errors": None})


    return jsonify({"upload_results": {"random_str": generate_random_str(), "folder_name": folder_name, "scores": scores, \
        "saved": saved, "rejected": rejected, "errors": errors, "saved_as": saved_as}, "upload_code": 119, "upload_message": \
            CODES_DICT[119], "system_errors": None})


@app.route('/upload_db', methods=["POST"])
@cross_origin()
def upload_db():
    if len(request.form) == 0:
        return jsonify({"result_code": 107, "result_message": CODES_DICT[107], "upload_results": None, "system_errors": None})

    if len(set(['upload_id', 'name', 'delete_pickles', 'rebuild_db', 'in_place']).intersection(set(request.form.keys()))) != 5:
        return jsonify({"result_code": 108, "result_message": CODES_DICT[108], "upload_results": None, "system_errors": None})

    id_folder = request.form['upload_id']
    id_ = id_folder.split("-")[0]
    name = "_".join([n.lower() for n in request.form['name'].split(" ")])
    delete_pickle = True if request.form['delete_pickles'].lower() == 'true' else False
    rebuild_db = True if request.form['rebuild_db'].lower() == 'true' else False
    in_place = True if request.form['in_place'].lower() == 'true' else False


    folder_path = os.path.join(os.getcwd(), temp['UPLOAD_FOLDER'], id_folder)
    log_to_file(f"Checking if folder {folder_path} exists, or is uploaded before.")
    if os.path.exists(f"{folder_path}_UPLOADED_TO_DB") or not os.path.exists(folder_path):
        log_to_file(f"Folder {folder_path} doesn't exist or has been uploaded before.", "ERROR")
        return jsonify({"result_code": 189, "result_message": CODES_DICT[189], \
            "upload_results": None, "system_errors": None})
      
    id_re_code, not_in_env, env_errs = main_id_regex(id_)

    if id_re_code != 126:
        return jsonify({"result_code": id_re_code, "result_message": CODES_DICT[id_re_code], \
            "upload_results": None, "system_errors": {"not_in_env": not_in_env, "env_errs": env_errs}})
    
    

    if platform.system == "Windows":
        imgs = glob.glob(folder_path + r"\*.[pj][np]*")
    else: 
        imgs = glob.glob(f"{folder_path}/*.[pj][np]*")

    message, message_pickle, rebuilt_db, res_main, res_aug, mysql_id = upload_to_db(imgs, id_, name, delete_pickle, rebuild_db, in_place)

    if message == 176:
        return jsonify({"result_code": message, "result_message": CODES_DICT[message], \
            "upload_results": None, "system_errors": {"not_in_env": res_main, "env_errs": res_aug}})
    
    if os.path.exists(folder_path):
        os.rename(folder_path, f"{folder_path}_UPLOADED_TO_DB")

    return jsonify({"result_code": message, "result_message": CODES_DICT[message], \
            "upload_results": {"mysql_id": mysql_id, "message_pickle": message_pickle, \
                "rebuilt_db": rebuilt_db, "resulting_imgs": {"main": res_main, "aug": res_aug}}, "system_errors": None})


  


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=8001, debug=True, use_reloader=False)