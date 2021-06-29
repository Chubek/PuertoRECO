from dotenv import dotenv_values
import pymongo 
from mtcnn import MTCNN
import cv2
import imgaug as ia
from imgaug import augmenters as iaa
import numpy as np

temp = dotenv_values(".env")


def verify_image(img_arr):
    detector = MTCNN()

    detection = detector.detect_faces(img_arr)

    if len(detection) == 0:
        return False

    return True

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

