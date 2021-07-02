from scripts.search_db import search_db
from scripts.verify_faces import verify_face
from scripts.upload_to_db import main_upload, verify_image
from scripts.prepare_img import prepare_img
from scripts import *
import pymongo
from dotenv import dotenv_values

temp = dotenv_values(".env")
dbclient = pymongo.MongoClient(temp["MONGO_URI"])


def main_reco(img_paths, id):
    split_img_paths = []

    for img in img_paths:
        prepared_imgs = prepare_img(img)

        split_img_paths.extend(prepared_imgs)

    if len(split_img_paths) == 0:
        return 630


    
    status, message = verify_face(dbclient, id, split_img_paths)

    if status:
        return message
    else:
        if message == 400:
            return message
        else:
            ids_names = search_db(split_img_paths)

            if ids_names:
                return ids_names
            else:
                return 100


def upload_to_db(imgs_path, id, name, delete_pickle):
    result, message = main_upload(dbclient, imgs_path, id, name, delete_pickle)

    return result, message
    
