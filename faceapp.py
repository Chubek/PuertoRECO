import os
from flask import Flask, request, render_template, send_from_directory, url_for, redirect, jsonify
from dotenv import dotenv_values
from main import *
import threading
import re
import base64
temp = dotenv_values(".env")
import glob
import platform
import time
from dotenv import dotenv_values

temp = dotenv_values(".env")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = temp["UPLOAD_FOLDER"]
 
    
@app.route('/verify', methods=['POST'])
def verify():
    id_folder = request.body['upload_id']
    id_ = id_folder.split("-")[0]

    skip_verify = True if request.body['skip_verify'].lower() == "true" else False
    skip_db_search = True if request.body['skip_db_search'].lower() == "true" else False
    skip_liveness = True if request.body['skip_liveness'].lower() == "true" else False

    if not re.match(r"{temp['ID_REGEX']}", id_):
        return jsonify({"recognition_code": 112, "recognition_results": None, "system_errors": None})

    folder_path = os.path.join(app.root_path, 'static', id_folder)

    if platform.system == "Windows":
        imgs = glob.glob(folder_path + r"\*.[pj][np]*")
    else: 
        imgs = glob.glob(f"{folder_path}/*.[pj][np]*")


    code, name, distancee = main_reco(imgs, id_, skip_liveness=skip_liveness, skip_verify=skip_verify, skip_db_search=skip_db_search)

    if code == 128:
        return jsonify({"recognition_code": 128, "recognition_results": None, "system_errors": {"not_in_env": name[0], "env_errs": name[1]}})

    return jsonify({"recognition_code": code, "recognition_results": {"name": name, "distance": distancee}, "system_errors": None})


@app.route('/upload_imgs', methods=['POST'])
def upload_verify():
    id_ = request.body['id']

    if not re.match(rf"{temp['ID_REGEX']}", id_):
        return jsonify({"upload_id": None, "message": "ID doesn't match pattern.", "upload_results": None})

    files = request.files

    if len(files) == 0:
        return jsonify({"upload_id": None, "message": "No files uploaded", "upload_results": None})

    folder_name = f"{id_}-{time.time()}"

    folder_path = os.path.join(app.root_path, 'static', id_)

    scores, saved, rejected, errors = assess_quality_and_save(request.files, folder_path)

    if scores == 128:
        return jsonify({"upload_id": None, "message": f"Sys error: .env file", "upload_results": {"not_in_env": saved, \
        "env_errs": rejected}})

    return jsonify({"upload_id": folder_name, "message": f"Files saved to {folder_path}.", "upload_results": {"scores": scores, \
        "saved": saved, "rejected": rejected, "errors": errors}})




@app.route('/upload_db', )
def upload_db():
    id_folder = request.body['upload_id']
    id_ = id_folder.split("-")[0]
    name = request.args['name']
    delete_pickle = True if request.args['dp'] == 'True' else False
    rebuild_db = True if request.args['rdb'] == 'True' else False

    if not re.match(r"{temp['ID_REGEX']}", id_) or not re.match("[a-z]+_[a-z]+", name):
        return jsonify({"result": "Name and/or ID do not match pattern", "message": None, "pickle_message": None, \
        "rebuild_db": None, "upload_results": None})


    folder_path = os.path.join(app.root_path, 'static', id_folder)

    if platform.system == "Windows":
        imgs = glob.glob(folder_path + r"\*.[pj][np]*")
    else: 
        imgs = glob.glob(f"{folder_path}/*.[pj][np]*")

    result, message, message_pickle, rebuilt_db, res_main, res_aug = upload_to_db(imgs, id_, name, delete_pickle, rebuild_db)

    if message == 128:
        return jsonify({"result": "Sys error: env", "message": message, "pickle_message": None, \
        "rebuild_db": None, "upload_results": {"not_in_env": result[0], "env_errs": result[1]}})
    
    return jsonify({"result": result, "message": message, "pickle_message": message_pickle, \
        "rebuild_db": rebuilt_db, "upload_results": {"res_main": res_main, "res_aug": res_aug}})



def run_app():
    app.run(host='0.0.0.0', debug=True, use_reloader=False)

if __name__ == '__main__':    
    threading.Thread(target=run_app).start()