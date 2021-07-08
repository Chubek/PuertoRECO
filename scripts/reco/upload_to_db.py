from dotenv import dotenv_values
from numpy.lib.npyio import save
import pymongo 
from mtcnn import MTCNN
import cv2
import imgaug as ia
from imgaug import augmenters as iaa
import numpy as np
import os
from datetime import datetime
from pathlib import Path
import random
from deepface import DeepFace
import functools
import operator
from scripts.utils.log_to_file import log_to_file
import platform
import glob
from scripts.database_op.db_op import insert_to_db

temp = dotenv_values(".env")
detector = MTCNN()

def verify_image(img_arr):
    detection = detector.detect_faces(img_arr)

    if len(detection) == 0 or len(detection) > 1:
        return []

    bb = detection[0]['box']
    face = img_arr[bb[1]:bb[1] + bb[3], bb[0]:bb[0] + bb[2]]
    return face

def resize_img(img_arr):
    width, height = int(temp["TARGET_WIDTH"]), int(temp["TARGET_WIDTH"])

    return cv2.resize(img_arr, (width, height))


def augment_img(img_arrs):
    seq = iaa.Sequential(
    [
        iaa.Sometimes(0.3, iaa.Fliplr(0.5)),  
        iaa.Sometimes(0.1, iaa.Crop(percent=(0, 0.1))),            
        iaa.Sometimes(0.5, iaa.GaussianBlur(sigma=(0, 0.5))),        
        iaa.Sometimes(0.7, iaa.contrast.LinearContrast((0.75, 1.5))),         
        iaa.Sometimes(0.8, iaa.AdditiveGaussianNoise(
            loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5)),    
        iaa.Sometimes(0.4, iaa.Multiply((0.8, 1.2), per_channel=0.2)),
        iaa.Sometimes(0.2, iaa.imgcorruptlike.Fog(severity=2)),
        iaa.Sometimes(0.6, iaa.imgcorruptlike.Saturate(severity=2)),
        iaa.Sometimes(0.1, iaa.imgcorruptlike.Pixelate(severity=2)), 
        iaa.Sometimes(0.5, iaa.MultiplyAndAddToBrightness(mul=(0.5, 1.5), add=(-30, 30)))
    ],
    random_order=True)  # apply augmenters in random order
    
    images_aug = []
    for _ in range(int(temp['NUM_AUG'])):
        images_aug.append(seq.augment_images(img_arrs))

    return functools.reduce(operator.iconcat, images_aug, [])


def hash_id_name(id, name):
    return hash(f"{id}_{name}")




def save_imgs(img_arrs, folder, id, augmented=False):
    main_folder = os.path.join(temp["DB_PATH"], folder)

    face_folder = os.path.join(main_folder, "faces")
    aug_folder = os.path.join(main_folder, "augmented_imgs")

    dt = datetime.now()
    au = "AUGMENTED" if augmented else "MAIN"
    saved_res = []

    save_path_dir = face_folder if not augmented else aug_folder

    
    if not os.path.exists(save_path_dir):
        os.makedirs(save_path_dir)
        log_to_file(f"Folder {save_path_dir} created.", "SUCCESS")

    for i, img in enumerate(img_arrs):
        save_path = os.path.join(save_path_dir, f"{au}_{i}_{id}_{dt.strftime('%m%d%Y')}.png")
        cv2.imwrite(save_path, img)
        log_to_file(f"{save_path} saved to file.", "INFO")
        saved_res.append(save_path)

    return saved_res


def main_upload(img_paths, id, name, delete_pickle, rebuild_db):
    log_to_file(f"Upload to db initiated with {len(img_paths)} images.", "INFO")

    arrs = [cv2.imread(path) for path in img_paths]

    deleted = 0

    for i in range(len(arrs)):     

        log_to_file(f"Detecting face for {img_paths[i]}", "INFO")
        img_det = verify_image(arrs[i - deleted])
        if len(img_det) == 0:
            log_to_file(f"Failed to detect face in image {img_paths[i]} at\
                 index {i} or there was more than one face... Removing and continuing.", "WARNING")
            del arrs[i - deleted]
            log_to_file(f"Image at index {i - deleted} removed. Length of the array is {len(arrs)}", "WARNING")
            deleted += 1
            if deleted == len(img_paths) or len(arrs) == 0:
                log_to_file(f"Failed to detect face in any of the images or all contained more than one face. Aborting upload.", "ERROR")
                return 152, None, None, None, None
            continue
        else:
            arrs[i - deleted] = img_det        

        log_to_file(f"Resizing images to {temp['TARGET_WIDTH']}x{temp['TARGET_WIDTH']}", "INFO")

        arrs[i - deleted] = resize_img(arrs[i - deleted])

        log_to_file(f"{img_paths[i]} successfully detected, cropped and resized.", "SUCCESS")

    log_to_file("Augmenting images...", "INFO")
    augs = augment_img(arrs)
    log_to_file(f"Got {len(augs)} augmented images.", "INFO")


    folder_name = f"{name}-{id}"

    log_to_file("Saving images...", "INFO")
    res_main = save_imgs(arrs, folder_name, id)
    res_aug = save_imgs(augs, folder_name, id, augmented=True)
    
    log_to_file(f"A total of {len(res_aug) + len(res_main)} images savd to {folder_name}", "SUCCESS")

    message_pickle = {"result": {"message": "You haven't set to delete any of the pickle files. This will create issues in the database.\
         Unless that was your intention, please delete the pickle files."}}
    
    rebuilt_db = {"result": {"message": "You have disabled delete_pickle so rebuild_db need not be enabled."}}

    log_to_file("Deleting pickle files...", "INFO")
    if delete_pickle:
        message_pickle = {"result": {"message": "delete_pickle enabled."}}

        pickle_files = glob.glob(f"{temp['DB_PATH']}/*.pkl")

        if platform.system() == 'Windows':
            pickle_files = glob.glob(temp['DB_PATH'] + r'\*.pkl')

        log_to_file(f"Following pickle files were found: {pickle_files}", "INFO")

        for pickle_file in pickle_files:
            pickle_file_name = Path(pickle_file).stem + ".pkl"
            if os.path.exists(pickle_file):
                os.remove(pickle_file)
                log_to_file(f"{pickle_file} removed.", "INFO")
                message_pickle['result'][pickle_file_name] = 670
            else:
                message_pickle['result'][pickle_file_name] = 604

        rebuilt_db = {"result": {"message:": "You have enabled delete_pickle, but you haven't enabled rebuild_db.\
             This will lead to slower operation in the next verify session."}}

        log_to_file(f"Rebuild db set to {rebuild_db}", "INFO")
        if rebuild_db:
            rebuilt_db = {"result": {'message': 'rebuild_db enabled.'}}
            script_folder = os.path.dirname(os.path.realpath(__file__))
            random_img = random.choice(os.listdir(os.path.join(script_folder, "rebuild_db_imgs")))
            for model_name in [m.strip() for m in temp['SELECTED_MODELS'].split(",")]:        
                _ = DeepFace.find(img_path = os.path.join(script_folder, "rebuild_db_imgs", random_img), db_path = temp["DB_PATH"],\
                     model_name = model_name, enforce_detection=False)

                rebuilt_db['result'][model_name] = 167
                log_to_file(f"DB for {model_name} rebuilt.", "INFO")




    log_to_file("Inserting to MySQL...", "INFO")
    try:
        id_db, message = insert_to_db(id, name, os.path.join(temp["DB_PATH"], folder_name))
        log_to_file("Successfully inserted into MySQL...", "SUCCESS")
    except:
        log_to_file("Insert into MySQL failed. Please check your settings.", "FAILURE")
        return 150, None, None, res_main, res_aug

    return message, message_pickle, rebuilt_db, res_main, res_aug, id_db