from scripts.utils.log_to_file import log_to_file
import cv2
from mtcnn import MTCNN
import os
from pathlib import Path
from scripts.reco.upload_to_db import augment_img

detector = MTCNN()

def crop_and_save(detection, img, save_path, img_name):
    paths = []
    for i, det in enumerate(detection):
        bb = det['box']

        log_to_file("Cropping face...")
        face = img[bb[1]:bb[1] + bb[3], bb[0]:bb[0] + bb[2]]
        
        face = cv2.resize(face, (224, 224))
        

        cv2.imwrite(os.path.join(save_path, f"{img_name}_{i}.png"), face)
        log_to_file(f"{os.path.join(save_path, f'{img_name}_{i}.png')} saved.", "SUCCESS")
        
        face_augmented = augment_img([face])
        
        for j, face_aug in enumerate(face_augmented):
            cv2.imwrite(os.path.join(save_path, f"{img_name}_{i}_{j}_AUGMENTED.png"), face_aug)            
            log_to_file(f"{os.path.join(save_path, f'{img_name}_{i}_{j}_AUGMENTED.png')} saved.", "SUCCESS")
            paths.append(os.path.join(save_path, f"{img_name}_{i}_{j}_AUGMENTED.png"))


        paths.append(os.path.join(save_path, f"{img_name}_{i}.png"))
        

    return paths


def prepare_img(img_path):
    img = cv2.imread(img_path)
    log_to_file(f"Getting face for {img_path}...", "INFO")

    detection = detector.detect_faces(img)

    if len(detection) == 0:
        log_to_file(f"Detection for {img_path} came up empty. Ignoring.", "WARNING")
    if len(detection) > 1:
        log_to_file(f"Multiple faces detected for {img_path}. If either of the images applies to ID, result is true.", "WARNING")

    save_path = Path(img_path).parent.absolute()
    img_name = Path(img_path).stem

    paths = crop_and_save(detection, img, save_path, img_name) 

    log_to_file(f"Found and saved {len(paths)} for {img_path}.", "SUCCESS")

    return paths

