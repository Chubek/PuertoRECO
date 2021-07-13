import cv2
import imquality.brisque as brisque
import numpy as np
from math import isclose
from scripts.utils.validate_env import validate_score_tol
import os
from scripts.utils.log_to_file  import log_to_file

def asses_img_quality(img_bytes, tol):
    log_to_file("Assessng score for uploaded image.", "INFO")
    
    try:
        img_arr = np.fromstring(img_bytes, np.uint8)
        img_enc = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        score = brisque.score(img_enc)

        log_to_file(f"Assessment successful, got an score of: {score}", "SUCCESS")

        if score <= tol:
            log_to_file(f"Score larger or equal to tolerance, returning success code.", "FINISH")
            return 119, score
        else:
            log_to_file(f"Score not larger or equal to tolerance, returning failure code.", "FAILURE")
            return 124, score
    except:
        log_to_file(f"Error reding score, or opening image. Assessment unsuccessful.", "ERROR")
        return 165, None