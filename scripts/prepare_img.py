import cv2
from mtcnn import MTCNN
import os

detector = MTCNN()

def crop_and_save(detection, img, save_path, img_name):
    paths = []
    for det in detection:
        bb = det['box']

        face = img[bb[1]:bb[1] + bb[3], bb[0]:bb[0] + bb[2]]

        cv2.imwrite(os.path.join(save_path, f"{img_name}.png"), face)

        paths.append(os.path.join(save_path, f"{img_name}.png"))

    return paths


def prepare_img(img_path):
    img = cv2.imread(img_path)
    detection = detector.detect_faces(img)

    save_path = img_path.split("/")[-2]
    img_name = img_path.split("/")[-1].split(".")[-2]

    if len(detection) == 0:
        return "No Images"

    paths = crop_and_save(detection, img, save_path, img_name)  

    return paths

