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
 
    
@app.route('/verify')
def verify():
    id_folder = request.args['id']
    id_ = id_folder.split("-")[0]

    if not re.match(r"{temp['ID_REGEX']}", id_):
        return jsonify({"recognition_result": 112})

    folder_path = os.path.join(app.root_path, 'static', id_folder)

    if platform.system == "Windows":
        imgs = glob.glob(folder_path + r"\*.[pj][np]*")
    else: 
        imgs = glob.glob(f"{folder_path}/*.[pj][np]*")

    print("Imgs found: " + imgs)

    result = main_reco(imgs, id)

    return jsonify({"recognition_result": result})


@app.route('/upload_verify', methods=['POST'])
def upload_verify():
    id_ = request.args['id']

    if not re.match(r"{temp['ID_REGEX']}", id_):
        return jsonify({"upload_id": None, "message": "ID doesn't match pattern."})

    files = request.files

    if len(request.files) == 0:
        return jsonify({"upload_id": None, "message": "No files uploaded"})

    folder_name = f"{id_}-{time.time()}"

    folder_path = os.path.join(app.root_path, 'static', id_)

    for uploaded_file in files:
        uploaded_file.save(folder_path, uploaded_file.filename)

    return jsonify({"upload_id": folder_name, "message": f"Files saved to {folder_path}. Pass the ID with verify?id=upload_id to verify.\
         Pass the ID with upload_db?id=upload_id&name=name&dp=True&rdb=True to upload to db. Files will be deleted after 24 hours."})




@app.route('/upload_db')
def upload_db():
    id_folder = request.args['id']
    id_ = id_folder.split("-")[0]
    name = request.args['name']
    delete_pickle = True if request.args['dp'] == 'True' else False
    rebuild_db = True if request.args['rdb'] == 'True' else False

    if not re.match(r"{temp['ID_REGEX']}", id_) or not re.match("[a-z]+_[a-z]+", name):
        return jsonify({"result": "Name and/or ID do not match pattern", "message": None, "pickle_message": None, \
        "rebuild_db": None, "res_main": None, "res_aug": None})


    folder_path = os.path.join(app.root_path, 'static', id_folder)

    if platform.system == "Windows":
        imgs = glob.glob(folder_path + r"\*.[pj][np]*")
    else: 
        imgs = glob.glob(f"{folder_path}/*.[pj][np]*")

    result, message, message_pickle, rebuilt_db, res_main, res_aug = upload_to_db(imgs, id_, name, delete_pickle, rebuild_db)

    return jsonify({"result": result, "message": message, "pickle_message": message_pickle, \
        "rebuild_db": rebuilt_db, "res_main": res_main, "res_aug": res_aug})

def run_app():
    app.run(host='0.0.0.0', debug=True, use_reloader=False)

if __name__ == '__main__':    
    threading.Thread(target=run_app).start()