import tensorflow.keras as keras
from scripts.liveness.download_and_load_model import down_load_model
import numpy as np
import cv2

def predict_spoof(img_paths):
    model = down_load_model()

    ret = []

    for img_path in img_paths:
        img = np.expand_dims(cv2.imread(img_path), axis=0)
        pred_res = model.predict(img)
        prob = pred_res[0]
        label = int(np.less_equal(0.700, prob))

        ret.append((label, prob))

    return ret


