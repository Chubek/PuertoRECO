from logging import log
from scripts.utils.log_to_file import *
from scripts.reco.search_db import search_db
from scripts.reco.verify_faces import verify_face
from scripts.reco.upload_to_db import main_upload, save_imgs, verify_image
from scripts.reco.prepare_img import prepare_img
from scripts import *
import pymongo
from scripts.liveness.predict_label import *
from dotenv import dotenv_values
import functools
import operator
import os
from scripts.utils.validate_env import validate_env
import re

temp = dotenv_values(".env")
dbclient = pymongo.MongoClient(temp["MONGO_URI"])




def main_reco(img_paths, id_):
    open_log_file()    
    val_res, not_in_env, env_errs = validate_env()

    if not val_res:
        close_log_file()
        return (121, not_in_env, env_errs)

    print(f"Starting recognition process with {len(img_paths)} images...")
    log_to_file(f"Starting recognition process with {len(img_paths)} images...", "INFO")
    face_img_paths = []

    if len(img_paths) == 0:
        log_to_file('Length of img_paths is zero. Aborting...', "ERROR")
        close_log_file()
        return 111

    prepared_imgs = [prepare_img(img) for img in img_paths]

    face_img_paths.extend(prepared_imgs)

    if len(face_img_paths) == 0:
        print("Could not detect a face in any of the images. Aborting...")
        log_to_file("Could not detect a face in any of the images. Aborting...", "ERROR")
        close_log_file()
        return 630

    face_img_paths = functools.reduce(operator.iconcat, face_img_paths, [])

    print(f"A total of {len(face_img_paths)} real and augmented images are ready for verification.")
    log_to_file(f"A total of {len(face_img_paths)} real and augmented images are ready for verification.", "INFO")

    liveness_pred = predict_spoof([f for f in face_img_paths if "AUGMENTED" not in f])

    len_spoof = len([label for label, _ in liveness_pred if label == 1])

    print(f"Found {len_spoof} spoof images.")
    log_to_file(f"Found {len_spoof} spoof images.", "WARNING")

    if len_spoof > 1:
        print("All of the images were spoof. Aborting...")
        log_to_file("All of the images were spoof. Aborting...", "ERROR")
        close_log_file()
        return 560
    
    status, message = verify_face(dbclient, id_, face_img_paths)

    if status:
        close_log_file()
        return message
    else:
        if message == 400:
            close_log_file()
            return message
        else:
            print("Image unverified... searching db...")
            log_to_file("Image unverified... searching db...", "INFO")
            ids_names = search_db(face_img_paths)
            print(f"Found ids and names: {ids_names}")
            if ids_names == True:
                for id__, _ in ids_names:
                    if id__ == id_:
                        print("ID matched with what was found in DB.")
                        log_to_file("ID matched with what was found in DB.", "SUCCESS")
                        close_log_file()
                        return 134
                    else:
                        print("ID didn't match.")
                        log_to_file("ID didn't match.", "FAILURE")
                        close_log_file()
                        return 100
            else:

                return 442


def upload_to_db(imgs_path, id_, name, delete_pickle, rebuild_db):
    open_log_file()
    val_res, not_in_env, env_errs = validate_env()

    if not val_res:
        close_log_file()
        return (121, not_in_env, env_errs)



    print(f"Starting upload to DB for id {id_} and name {name}")
    log_to_file(f"Starting upload to DB for id {id_} and name {name}", "INFO")
    if len(imgs_path) == 0:
        close_log_file()
        return "Length of imgs list was 0", None, None, None, None, None
    
    result, message, message_pickle, rebuilt_db, res_main, res_aug = main_upload(dbclient, imgs_path, id_, name, delete_pickle, rebuild_db)

    print("Upload to DB done.")
    log_to_file("Upload to DB done.", "SUCCESS")
    close_log_file()
    return result, message, message_pickle, rebuilt_db, res_main, res_aug

print(upload_to_db([r"I:\face_reco\test_imgs\father\IMG_20200807_231734.jpg", r"I:\face_reco\test_imgs\father\IMG_20200808_175514.jpg",\
   #  r'I:\face_reco\test_imgs\father\IMG_20210602_140503.jpg'],\
    # 'RECO_ID_001', "father", True, True))
#print(main_reco([r"I:\face_reco\test_imgs\father\IMG_20210602_140505.jpg", r"I:\face_reco\test_imgs\father\IMG_20210602_140508.jpg"], "RECO_ID_001"))
    
