import cv2
import os
import numpy as np
from dotenv import dotenv_values

temp = dotenv_values(".env")


def read_img(img_path):
    return cv2.imread(img_path)

def crop_and_resize(img, bboxes):
    ret = []

    for box in bboxes:
        img_face = img[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]
        img_face_resized = cv2.resize(img_face, (int(temp["IMG_WIDTH"]), int(temp["IMG_HEIGHT"])))
        
        img_expanded = np.expand_dims(img_face_resized, axis=0)

        ret.append((box, img_expanded))

    return ret

def put_rect_with_box(img, box_and_classes):
    for box_class in box_and_classes:
        box, label_prob = box_class
        x, y, w, h = box
        label, prob = label_prob
        print("label_inner", "prob_inner", label, prob)
        color = {0: (34,139,34), 1: (178,34,34)}

        img = cv2.rectangle(img, (x, y), (x + w, y + h), color[label], 1)        
        
        dict_labels = {0: 'Live', 1: 'Spoof'}

        label_text = f"{dict_labels[label]}|{prob}"
        cv2.putText(img, label_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color[label], 2)

    return img