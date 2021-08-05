from PIL import Image
from io import BytesIO
import os
import cv2
import numpy as np
import glob
import platform

def save_bytes_as_png(byte_data, image_path):
    if not os.path.exists(os.path.basename(image_path)):
        os.makedirs(os.path.basename(image_path))    
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    img.save(image_path, "PNG")



def make_video(path, video_save):
    if not os.path.exists(video_save):
        os.makedirs(video_save)

    img_array = []
    if platform.system == "Windows":
        files = glob.glob(path + r"\*.png")
    else:
        files = glob.glob(f"{path}\*.png")

    for filename in files:
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

    out = cv2.VideoWriter(f'{video_save}',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()