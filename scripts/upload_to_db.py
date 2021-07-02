from dotenv import dotenv_values
import pymongo 
from mtcnn import MTCNN
import cv2
import imgaug as ia
from imgaug import augmenters as iaa
import numpy as np
import os
from datetime import datetime

temp = dotenv_values(".env")


def verify_image(img_arr):
    detector = MTCNN()

    detection = detector.detect_faces(img_arr)

    if len(detection) == 0 or len(detection) > 1:
        return False

    bb = detection['box']
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

    images_aug = seq.augment_images(img_arrs)

    return images_aug


def hash_id_name(id, name):
    return hash(f"{id}_{name}")

def insert_to_db(mongo_client, id, name, db_path):
    db = mongo_client[temp["MONGO_DB"]]
    col= mongo_client[temp["MONO_COLL"]]

    insert_dict = {"reco_id": id, "person_name": name, "db_path": db_path }

    update_query = { "reco_id": id }

    if len(col.find_one(update_query)) >= 1:        
        newvalues = { "$set": { "person_name": name, "db_path": db_path } }
        
        col.update_one(update_query, newvalues)

        return None, "Updated"
    
    x = col.insert_one(insert_dict)

    return x, "Inserted"


def save_imgs(img_arrs, folder, id, augmented=False):
    main_folder = os.path.join(temp["DB_PATH"], folder)
    dt = datetime.now()
    au = "AUGMENTED" if augmented else "MAIN"
    for i, img in enumerate(img_arrs):
        cv2.imwrite(os.path.join(main_folder, f"{au}_{i}_{id}_{dt.strftime('%m/%d/%Y')}.png"), img)


def main_upload(mongo_client, img_paths, id, name):
    arrs = [cv2.imread(path) for path in img_paths]

    for i in range(len(arrs)):
        img_det = verify_image(arrs[i])
        if not img_det:
            del arrs[i]
        else:
            arrs[i] = img_det

        arrs[i] = resize_img(arrs[i])


    augs = augment_img(arrs)

    folder_name = f"{name}_{id}_{hash_id_name(id, name)}"


    save_imgs(arrs, folder_name, id)
    save_imgs(augs, folder_name, id, augmented=True)

    return insert_to_db(mongo_client, id, name, os.path.join(temp["DB_PATH"], folder_name))