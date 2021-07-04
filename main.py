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
    print(f"Starting recognition process with {len(img_paths)} images...")
    log_to_file(f"Starting recognition process with {len(img_paths)} images...", "INFO")

    val_res, not_in_env, env_errs = validate_env()

    if not val_res:        
        return [not_in_env, env_errs], None

    for img in img_paths:
        if not os.path.exists(img):
            print(f"File {img} doesn't exist.")
            log_to_file(f"File {img} doesn't exist.", "FAILURE")
            return 159, None
    
    if len(img_paths) == 0:
        log_to_file('Length of img_paths is zero. Aborting...', "ERROR")        
        return 111, None

    prepared_imgs = [prepare_img(img) for img in img_paths]    

    face_img_paths = functools.reduce(operator.iconcat, prepared_imgs, [])

    if len(face_img_paths) == 0:
        print("Could not detect a face in any of the images. Aborting...")
        log_to_file("Could not detect a face in any of the images. Aborting...", "ERROR")
        
        return 630, None

    print(f"A total of {len(face_img_paths)} real and augmented images are ready for verification.")
    log_to_file(f"A total of {len(face_img_paths)} real and augmented images are ready for verification.", "INFO")

    liveness_pred = predict_spoof([f for f in face_img_paths if "AUGMENTED" not in f])

    len_spoof = len([label for label, _ in liveness_pred if label == 1])

    print(f"Found {len_spoof} spoof images.")
    log_to_file(f"Found {len_spoof} spoof images.", "WARNING")

    if len_spoof >= len([f for f in face_img_paths if "AUGMENTED" not in f]):
        print("All faces were spoof. Aborting...")
        log_to_file("All faces were spoof. Aborting...", "ERROR")
        
        return 560, None
    
    status, message = verify_face(dbclient, id_, face_img_paths)

    if status:        
        print(f"ID {id_} verified and got name {status}")
        log_to_file(f"ID {id_} verified and got name {status}", "FINISH") 
        return message, status
    else:
        if message != 500:
                       
            return message, None
        else:
            print("Image unverified... searching db...")
            log_to_file("Image unverified... searching db...", "INFO")
            ids_names = search_db(face_img_paths)
            print(f"Found ids and names: {ids_names}")
            if ids_names == True:
                for id__, name in ids_names:
                    if id__ == id_:
                        print(f"ID {id_} matched with what was found in DB.")
                        log_to_file("ID {id_} matched with what was found in DB.", "FINISH")
                        
                        return 134, name
                    else:
                        print("ID didn't match.")
                        log_to_file("ID didn't match.", "FAILURE")
                        
                        return 100, None
            else:
                return 442, None


def upload_to_db(imgs_path, id_, name, delete_pickle, rebuild_db):
    print(f"Starting upload to DB for id {id_} and name {name}")
    log_to_file(f"Starting upload to DB for id {id_} and name {name}", "INFO")
    
    val_res, not_in_env, env_errs = validate_env()

    if not val_res:        
        return [not_in_env, env_errs]

        
    for img in imgs_path:
        if not os.path.exists(img):
            print(f"File {img} doesn't exist.")
            log_to_file(f"File {img} doesn't exist.", "FAILURE")
            return f"File {img} doesn't exist.", None, None, None, None, None

    
    if len(imgs_path) == 0:
        print("Length of the given images array was 0.")
        log_to_file("Length of the given images array was 0.", "FAILURE")
        return "Length of imgs list was 0", None, None, None, None, None
    
    result, message, message_pickle, rebuilt_db, res_main, res_aug = main_upload(dbclient, imgs_path, id_, name, delete_pickle, rebuild_db)

    print("Upload to DB done.")
    log_to_file("Upload to DB done.", "FINISH")
    
    return result, message, message_pickle, rebuilt_db, res_main, res_aug

open_log_file()
#print(upload_to_db([r"I:\face_reco\test_imgs\daeemajeed1.png", r"I:\face_reco\test_imgs\daeemajeed2.png", r"I:\face_reco\test_imgs\daeemajeed3.png"],\
  # 'RECO_ID_004', "majeed", True, True))
print(main_reco([r"I:\face_reco\test_imgs\daeemajeed4.png"], "RECO_ID_004"))
    
close_log_file()