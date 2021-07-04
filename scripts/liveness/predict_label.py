import tensorflow.keras as keras
from scripts.liveness.download_and_load_model import down_load_model
import numpy as np
import cv2
from scripts.utils.log_to_file import log_to_file

def predict_spoof(img_paths):
    model = down_load_model()

    ret = []

    for img_path in img_paths:
        print(f"Detecting liveness on {img_path}")
        log_to_file(f"Detecting liveness on {img_path}", "INFO")
        img = np.expand_dims(cv2.imread(img_path), axis=0)
        pred_res = model.predict(img)
        prob = pred_res[0]
        label = int(np.less_equal(0.700, prob))
        print(f"For {img_path} got probability, label: {prob}, {label}")
        log_to_file(f"For {img_path} got probability, label: {prob}, {label}", "INFO")
        ret.append((label, prob))

    return ret


