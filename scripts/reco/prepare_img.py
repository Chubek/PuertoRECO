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

        print("Cropping face...")
        face = img[bb[1]:bb[1] + bb[3], bb[0]:bb[0] + bb[2]]
        
        face = cv2.resize(face, (224, 224))
        

        cv2.imwrite(os.path.join(save_path, f"{img_name}_{i}.png"), face)
        
        face_augmented = augment_img([face])
        
        for j, face_aug in enumerate(face_augmented):
            cv2.imwrite(os.path.join(save_path, f"{img_name}_{i}_{j}_AUGMENTED.png"), face_aug)
            paths.append(os.path.join(save_path, f"{img_name}_{i}_{j}_AUGMENTED.png"))

        paths.append(os.path.join(save_path, f"{img_name}_{i}.png"))
        

    return paths


def prepare_img(img_path):
    img = cv2.imread(img_path)
    print(f"Getting face for {img_path}...")
    log_to_file(f"Getting face for {img_path}...", "INFO")
    detection = detector.detect_faces(img)

    if len(detection) == 0:
        print(f"Detection for {img_path} came up empty. Ignoring.")
        log_to_file(f"Detection for {img_path} came up empty. Ignoring.", "WARNING")
    if len(detection) > 1:
        print(f"Multiple faces detected for {img_path}. If either of the images applies to ID, result is true.")
        log_to_file(f"Multiple faces detected for {img_path}. If either of the images applies to ID, result is true.", "WARNING")

    save_path = Path(img_path).parent.absolute()
    img_name = Path(img_path).stem

    paths = crop_and_save(detection, img, save_path, img_name) 

    print(f"Found {len(paths)} for {img_path}.") 
    log_to_file(f"Found {len(paths)} for {img_path}.", "INFO")

    return paths

