from unit_tests.params import NAME
from deepface import DeepFace
import glob
from dotenv import dotenv_values
from scripts.database_op.db_op import select_from_db
import platform
from scripts.utils.log_to_file import log_to_file
from math import isclose
from pathlib import Path
import os

temp = dotenv_values(".env")

def verify_face(mongo_client, id_, img_paths):
    log_to_file(f"Verifying {len(img_paths)} images...", "INFO")
    
    try:
        _, name, path = select_from_db(id_)
    except:
        log_to_file("Problem getting ID, please check MySQL settings.", "ERROR")
        False, 116, None

    if not os.path.exists(path):
        return False, 113, None          
   

    images_db_aug = glob.glob(f"{path}/augmented_imgs/*.png")
    images_db_normal = glob.glob(f"{path}/faces/*.png")

    if platform.system() == "Windows":
        images_db_aug = glob.glob(path + r"\augmented_imgs\*.png")
        images_db_normal = glob.glob(path + r"\faces\*.png")        

    log_to_file(f"Found {len(images_db_aug)} augmented images and {len(images_db_normal)} real images in DB.", "INFO")

    images_paths_aug = [img for img in img_paths if "AUGMENTED" in img]
    images_paths_normal = [img for img in img_paths if not "AUGMENTED" in img]
    
    log_to_file(f"Found {len(images_paths_aug)} augmented images and {len(images_paths_normal)} real images in img_paths.", "INFO")


    verified = 0
    verified_aug = 0

    for model_name in [m.strip() for m in temp["SELECTED_MODELS"].split(',')]:
        log_to_file(f"Model {model_name} selected.", "INFO")
        for img_p_n in images_paths_normal:
            for img_db_n in images_db_normal:
                log_to_file(f"Verifying on real test image {img_p_n} and real DB image {img_db_n}", "INFO")
                result = DeepFace.verify(img_p_n, img_db_n, model_name = model_name, enforce_detection=False)

                if result['verified']:
                    verified += 1                    
                    log_to_file(f"ID {id_} verified for the {verified}th time with real image on verification image {img_p_n} and db image {img_db_n} with model {model_name} and distance of\
                         {result['distance']} and a threshold of {str(result['max_threshold_to_verify']).strip()}.", "INFO")

                    if verified >= int(temp['VER_TOL']) or verified >= len(images_paths_normal):
                        log_to_file(f"Real verification reached the tolerance of {temp['VER_TOL']}. Verifying...", "SUCCESS")
                        return name, 200, result['distance']

        log_to_file('Failed to verify on real images, trying augmented ones...', "FAILURE")    

        for img_p_a in images_paths_aug:
            for img_db_a in images_db_aug + images_db_normal:
                log_to_file(f"Verifying on augmented test image {img_p_a} and augmented/real DB image {img_db_a}", "INFO")
                result = DeepFace.verify(img_p_a, img_db_a, model_name = model_name, enforce_detection=False)

                if result['verified']:
                    verified_aug += 1                        
                    log_to_file(f"ID {id_} verified for the {verified_aug}th time with augmented image on verification image {img_p_a} and db image {img_db_a} with model {model_name} and distance of\
                            {result['distance']} and a threshold of {str(result['max_threshold_to_verify']).strip()}.", "INFO")

                if verified_aug >= int(temp['VER_TOL_AUG']):
                    log_to_file(f"Augmentation verification reached the tolerance of {temp['VER_TOL_AUG']}. Verifying...", "SUCCESS")
                    return name, 200, result['distance']

        log_to_file('Failed to verify on augmented images.', "FAILURE")    
                  

    return False, 500, None