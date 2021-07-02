import cv2
from mtcnn import MTCNN
import os

detector = MTCNN()


def handle_multiple(img_path):
    img = cv2.imread(img_path)
    detection = detector.detect_faces(img)

    if len(detection) == 1:
        return False

    save_path = img_path.split("/")[-2]
    img_name = img_path.split("/")[-1].split(".")[-2]

    paths = []

    for det in detection:
        bb = det['box']

        face = img[bb[1]:bb[1] + bb[3], bb[0]:bb[0] + bb[2]]

        cv2.imwrite(os.path.join(save_path, f"{img_name}.png"), face)

        paths.append(os.path.join(save_path, f"{img_name}.png"))

    return paths

