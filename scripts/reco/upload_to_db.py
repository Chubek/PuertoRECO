from dotenv import dotenv_values
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
import log_to_file

temp = dotenv_values(".env")


def verify_image(img_arr):
    detector = MTCNN()

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
        iaa.Fliplr(0.5),  
        iaa.Crop(percent=(0, 0.1)),            
        iaa.Sometimes(0.5, iaa.GaussianBlur(sigma=(0, 0.5))),        
        iaa.ContrastNormalization((0.75, 1.5)),         
        iaa.AdditiveGaussianNoise(
            loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5),    
        iaa.Multiply((0.8, 1.2), per_channel=0.2),
        iaa.Affine(
            scale={
                "x": (0.8, 1.2),
                "y": (0.8, 1.2)
            },
            translate_percent={
                "x": (-0.2, 0.2),
                "y": (-0.2, 0.2)
            },
            rotate=(-25, 25),
            shear=(-8, 8))
    ],
    random_order=True)  # apply augmenters in random order
    
    images_aug = []
    for _ in range(int(temp['NUM_AUG'])):
        images_aug.append(seq.augment_images(img_arrs))

    return functools.reduce(operator.iconcat, images_aug, [])


def hash_id_name(id, name):
    return hash(f"{id}_{name}")

def insert_to_db(mongo_client, id, name, db_path):
    db = mongo_client[temp["MONGO_DB"]]
    col= db[temp["MONGO_COLL"]]

    insert_dict = {"reco_id": id, "person_name": name, "db_path": db_path }

    update_query = { "reco_id": id }

    if col.find_one(update_query) is not None:        
        newvalues = { "$set": { "person_name": name, "db_path": db_path } }
        
        col.update_one(update_query, newvalues)

        return None, 900
    
    x = col.insert_one(insert_dict)

    return x.inserted_id, 800


def save_imgs(img_arrs, folder, id, augmented=False):
    main_folder = os.path.join(temp["DB_PATH"], folder)
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
    dt = datetime.now()
    au = "AUGMENTED" if augmented else "MAIN"
    saved_res = []
    for i, img in enumerate(img_arrs):
        cv2.imwrite(au + ".png", img)
        cv2.imwrite(os.path.join(main_folder, f"{au}_{i}_{id}_{dt.strftime('%m%d%Y')}.png"), img)
        saved_res.append(os.path.join(main_folder, f"{au}_{i}_{id}_{dt.strftime('%m%d%Y')}.png"))

    return saved_res


def main_upload(mongo_client, img_paths, id, name, delete_pickle, rebuild_db):
    print(f"Upload to db initiated with {len(img_paths)} images.")
    log_to_file(f"Upload to db initiated with {len(img_paths)} images.", "Info")

    arrs = [cv2.imread(path) for path in img_paths]

    deleted = 0

    for i in range(len(arrs)):
        print(f"Detecting face for {img_paths[i]}")
        log_to_file(f"Detecting face for {img_paths[i]}", "Info")
        img_det = verify_image(arrs[i])
        if len(img_det) == 0:
            print(f"Failed to detect face in image {img_paths[i]}... Removing.")
            log_to_file(f"Failed to detect face in image {img_paths[i]}... Removing.", "Warning")
            del arrs[i]
            deleted += 1

            if deleted == len(img_paths):
                print(f"Failed to detect face in any of the images. Aborting upload.")
                log_to_file(f"Failed to detect face in any of the images. Aborting upload.", "Error")
                return "Could not detect a face in any of the images", 150, 605, None, None
        else:
            arrs[i] = img_det
        print("Resizing images to {temp['TARGET_WIDTH']}x{temp['TARGET_WIDTH']}")
        arrs[i] = resize_img(arrs[i])

    print("Augmenting images...")
    augs = augment_img(arrs)
    print(f"Got {len(augs)} augmented images.")
    folder_name = f"{name}-{id}"

    print("Saving images...")
    res_main = save_imgs(arrs, folder_name, id)
    res_aug = save_imgs(augs, folder_name, id, augmented=True)
    print("Images saved.")

    log_to_file(f"A total of {len(res_aug) + len(res_main)} images savd to {folder_name}")

    message_pickle = {"result": {"message": "You haven't set to delete any of the pickle files. This will create issues in the database.\
         Unless that was your intention, please delete the pickle files."}}
    
    rebuilt_db = {"result": {"message": "You have disabled delete_pickle so rebuild_db need not be enabled."}}

    print("Deleting pickle files...")
    if delete_pickle:
        message_pickle = {"result": {"message": "delete_pickle enabled."}}

        for pickle_file in (temp['PICKLE_PATH_1'], temp['PICKLE_PATH_2'], temp['PICKLE_PATH_3']):
            pickle_file_name = Path(pickle_file).stem + ".pkl"
            if os.path.exists(pickle_file):
                os.remove(pickle_file)
                print(f"{pickle_file} removed.")
                message_pickle['result'][pickle_file_name] = 670
            else:
                message_pickle['result'][pickle_file_name] = 604

        rebuilt_db = {"result": {"message:": "You have enabled delete_pickle, but you haven't enabled rebuild_db.\
             This will lead to slower operation in the next verify session."}}

        print(f"Rebuild db set to {rebuild_db}")
        if rebuild_db:
            rebuilt_db = {"result": {'message': 'rebuild_db enabled.'}}
            script_folder = os.path.dirname(os.path.realpath(__file__))
            random_img = random.choice(os.listdir(os.path.join(script_folder, "rebuild_db_imgs")))
            for model_name in (temp["SELECTED_MODEL_1"], temp["SELECTED_MODEL_2"], temp["SELECTED_MODEL_3"]):        
                _ = DeepFace.find(img_path = os.path.join(script_folder, "rebuild_db_imgs", random_img), db_path = temp["DB_PATH"],\
                     model_name = model_name, enforce_detection=False)

                rebuilt_db['result'][model_name] = 167
                print(f"DB for {model_name} rebuilt.")





    id_db, message = insert_to_db(mongo_client, id, name, os.path.join(temp["DB_PATH"], folder_name))

    return id_db, message, message_pickle, rebuilt_db, res_main, res_aug