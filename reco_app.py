import os
from flask import Flask, jsonify, send_from_directory, request
from dotenv import dotenv_values
from main import *
import threading
import re
import glob

temp = dotenv_values(".env")

app = Flask(__name__)


@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/verify')
def verify():
    id = request.args['id']

    folder_path = os.path.join(app.root_path, 'static', id)

    imgs = glob.glob(f"{folder_path}/*.[pj][np]*")

    result = main_reco(imgs, id)

    return jsonify({"reco_result": result})


@app.route('/upload_verify', methods=['POST'])
def upload_verify():
    id = request.args['id']

    files = request.files

    if len(request.files) == 0:
        return jsonify({"message": "No files uploaded"})

    folder_path = os.path.join(app.root_path, 'static', id)

    for uploaded_file in files:
        uploaded_file.save(folder_path, uploaded_file.filename)

    return jsonify({"message": f"Files saved to {folder_path}. Pass the ID with verify?id=id to verify.\
         Pass the ID with upload_db?id=id&name=name&dp=True to upload to db. Files will be deleted after 24 hours."})




@app.route('/upload_db')
def upload_db():
    id = request.args['id']
    name = request.args['name']
    delete_pickle = True if request.args['dp'] == 'True' else False


    folder_path = os.path.join(app.root_path, 'static', id)

    imgs = glob.glob(f"{folder_path}/*.[pj][np]*")

    result = upload_to_db(imgs, id, name, delete_pickle)

    return jsonify({"reco_result": result})



