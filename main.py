from glob import glob
from logging import log
from scripts.utils.log_to_file import *
from scripts.reco.search_db import search_db
from scripts.reco.verify_faces import verify_face
from scripts.reco.upload_to_db import main_upload, save_imgs, verify_image
from scripts.reco.prepare_img import prepare_img
from scripts import *
import pymongo
from scripts.liveness.predict_label import *
import functools
import operator
import os
from scripts.utils.validate_env import validate_env, validate_mongo_env




def main_reco(img_paths, id_, test_title=None, skip_verify=False, skip_db_search=False):    
    test_str = "This is the real deal!" if not test_title else f"Test mode, test title: {test_title}"
    log_to_file(f"Starting recognition process with {len(img_paths)} images... {test_str}", "INFO")

    if skip_verify and skip_db_search:
        log_to_file("Both skip_verify and skip_db_search set to True. One must be False. Aborting...", "ERROR")
        return 143, None, None

    dbclient, not_in_env, env_errs = dbclient_tuple

    if not dbclient:  
        return 128, [not_in_env, env_errs], None
    

    temp, not_in_env, env_errs = validate_env(os.path.dirname(os.path.realpath(__file__)))

    if not temp:        
        return 128, [not_in_env, env_errs], None

    for img in img_paths:
        if not os.path.exists(img):
            log_to_file(f"File {img} doesn't exist.", "FAILURE")
            return 159, None, None
    
    if len(img_paths) == 0:
        log_to_file('Length of img_paths is zero. Aborting...', "ERROR")        
        return 111, None, None

    prepared_imgs = [prepare_img(img) for img in img_paths]    

    face_img_paths = functools.reduce(operator.iconcat, prepared_imgs, [])

    if len(face_img_paths) == 0:
        log_to_file("Could not detect a face in any of the images. Aborting...", "ERROR")
        
        return 630, None, None

    log_to_file(f"A total of {len(face_img_paths)} real and augmented images are ready for verification.", "INFO")

    liveness_pred = predict_spoof([f for f in face_img_paths if "AUGMENTED" not in f])

    if type(liveness_pred) == int:
        return liveness_pred, None, None

    len_spoof = len([label for label, _ in liveness_pred if label == 1])

    log_to_file(f"Found {len_spoof} spoof images.", "WARNING")

    if len_spoof >= len([f for f in face_img_paths if "AUGMENTED" not in f]):
        log_to_file("All faces were spoof. Aborting...", "ERROR")
        
        return 560, None, None
    
    if not skip_verify:
        log_to_file("skip_verify set to False, verifying...", "INFO")
        status, message, distance = verify_face(dbclient, id_, face_img_paths)
    else:
        log_to_file("skip_verify set to True. Skipping verification.", "INFO")
        status, message, distance = False, 500, None

    if status:        
        log_to_file(f"ID {id_} verified and got name {status}", "FINISH") 
        return message, status, distance
    else:
        if message != 500:                       
            return message, None, None
        else:
            if not skip_db_search:
                log_to_file("Image unverified... searching db...", "INFO")
                ids_names_distances = search_db(face_img_paths)
                if len(ids_names_distances) != 0:
                    for name, id__, distance in ids_names_distances:
                        if id__ == id_:
                            log_to_file(f"ID {id_} matched with what was found in DB and got distance {distance}.", "FINISH")
                        
                            return 134, name, distance
                        else:
                            log_to_file("ID didn't match.", "FAILURE")
                        
                            return 100, None, None
            else:
                log_to_file("skip_db_search is enabled. Skipping db search and returning results.", "FAILURE")
                return message, status, distance
                


def upload_to_db(imgs_path, id_, name, delete_pickle, rebuild_db, test_title=None):
    test_str = "This is the real deal!" if not test_title else f"Test mode, test title: {test_title}"
    log_to_file(f"Starting upload to DB for id {id_} and name {name}... {test_str}", "INFO")
    
    dbclient, not_in_env, env_errs = dbclient_tuple

    if not dbclient:  
        return [not_in_env, env_errs], 128, None, None, None, None

    temp, not_in_env, env_errs = validate_env(os.path.dirname(os.path.realpath(__file__)))

    if not temp:        
        return [not_in_env, env_errs], 128, None, None, None, None

        
    for img in imgs_path:
        if not os.path.exists(img):
            log_to_file(f"File {img} doesn't exist.", "FAILURE")
            return f"File {img} doesn't exist.", 987, None, None, None, None

    
    if len(imgs_path) == 0:
        log_to_file("Length of the given images array was 0.", "FAILURE")
        return "Length of imgs list was 0", 981, None, None, None, None
    
    result, message, message_pickle, rebuilt_db, res_main, res_aug = main_upload(dbclient, imgs_path, id_, name, delete_pickle, rebuild_db)

    log_to_file("Upload to DB done.", "FINISH")
    
    return result, message, message_pickle, rebuilt_db, res_main, res_aug

