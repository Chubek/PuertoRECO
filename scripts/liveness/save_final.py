import cv2
from dotenv import dotenv_values
import time
import os

temp = dotenv_values(".env")


def save_final_imgs(img_array):
    if not os.path.exists(temp["OUTPUT_FOLDER"]):
        os.makedirs(temp["OUTPUT_FOLDER"])

    hash_val = hash(str(time.time()).encode("UTF-8"))
    print("Saving to: ", f'{temp["OUTPUT_FOLDER"]}/{hash_val}.jpg')    
    cv2.imwrite(f'{temp["OUTPUT_FOLDER"]}/{hash_val}.jpg', img_array)

    return f'/outputs/{hash_val}.jpg'


