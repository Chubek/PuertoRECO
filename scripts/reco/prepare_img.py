from scripts.utils.log_to_file import log_to_file
import cv2
from mtcnn import MTCNN
import os
from pathlib import Path
from scripts.reco.upload_to_db import augment_img
from deepface import DeepFace

detector = MTCNN()

def crop_and_save(detection, img, save_path, img_name):
    paths = []
    aug_folder = os.path.join(save_path, "augmented_imgs")
    face_folder = os.path.join(save_path, "faces")

    for ff in [aug_folder, face_folder]:
        if not os.path.exists(ff):
            os.makedirs(ff)
            log_to_file(f"Folder {ff} created.", "SUCCESS")

    


    log_to_file(f"Cropping face for {img_name}...", "INFO")
    face = img[detection['y']:detection['y'] + detection['h'], detection['x']:detection['x'] + detection['w']]
        
    face = cv2.resize(face, (224, 224))
        

    cv2.imwrite(os.path.join(face_folder, f"{img_name}.png"), face)
    log_to_file(f"{os.path.join(face_folder, f'{img_name}.png')} saved.", "SUCCESS")    
    paths.append(os.path.join(face_folder, f"{img_name}.png"))
        
    face_augmented = augment_img([face])
        
    for j, face_aug in enumerate(face_augmented):
        cv2.imwrite(os.path.join(aug_folder, f"{img_name}_{j}_AUGMENTED.png"), face_aug)            
        log_to_file(f"{os.path.join(aug_folder, f'{img_name}_{j}_AUGMENTED.png')} saved.", "SUCCESS")
        paths.append(os.path.join(aug_folder, f"{img_name}_{j}_AUGMENTED.png"))


        

    return paths


def prepare_img(img_path):
    img = cv2.imread(img_path)
    log_to_file(f"Getting face for {img_path}...", "INFO")

    try:
        detection = DeepFace.analyze(img_path, detector_backend = 'mtcnn')['region']
    except:
        log_to_file(f"{img_path} failed to detect a face.")
        return []

    save_path = Path(img_path).parent.absolute()
    img_name = Path(img_path).stem

    paths = crop_and_save(detection, img, save_path, img_name) 

    log_to_file(f"Found and saved {len(paths)} for {img_path}.", "SUCCESS")

    return paths

