from deepface import DeepFace
import glob
from dotenv import dotenv_values
import pymongo
import platform
from scripts.utils.log_to_file import log_to_file
from math import isclose
from pathlib import Path

temp = dotenv_values(".env")

def verify_face(mongo_client, id_, img_paths):
    print("Files to verify: " + str(img_paths) + " with length " + str(len(img_paths)))
    log_to_file("Files to verify: " + str(img_paths) + " with length " + str(len(img_paths)), "INFO")
    
    try:
        db = mongo_client[temp["MONGO_DB"]]
        coll= db[temp["MONGO_COLL"]]
        row = coll.find_one({"reco_id": id_})
    except:
        False, 116

    name = str(Path(row['db_path']).parts[-1]).split("-")[0]

    if row is None:
        print("Didn't find the ID in the database.")
        log_to_file("Didn't find the ID in the database.", "ERROR")
        return False, 400

    if platform.system() == "Windows":
        images = glob.glob(row['db_path'] + r"\*.png")
    else:
        images = glob.glob(f"{row['db_path']}/*.png")

    print("Images found in db: " + str(images) + " with length " + str(len(images)))
    log_to_file("Images found in db: " + str(images) + " with length " + str(len(images)), "INFO")

    images_db_aug = [img for img in images if "AUGMENTED" in img]
    images_db_normal = [img for img in images if not "AUGMENTED" in img]
    images_paths_aug = [img for img in img_paths if "AUGMENTED" in img]
    images_paths_normal = [img for img in img_paths if not "AUGMENTED" in img]
    
    print(f"DB set split into {len(images_db_normal)} normal images and {len(images_db_aug)}")
    print(f"Test set split into {len(images_paths_normal)} normal images and {len(images_paths_aug)}")
    log_to_file(f"DB set split into {len(images_db_normal)} normal images and {len(images_db_aug)} augmented images.", "INFO")
    log_to_file(f"Test set split into {len(images_paths_normal)} normal images and {len(images_paths_aug)} augmented images.", "INFO")


    verified = 0
    verified_aug = 0

    for model_name in [m.strip() for m in temp["SELECTED_MODELS"].split(',')]:
        print(f"Trying model {model_name}")
        for img_p_n in images_paths_normal:
            for img_db_n in images_db_normal:
                result = DeepFace.verify(img_p_n, img_db_n, model_name = model_name, enforce_detection=False)

                if result['verified']:
                    verified += 1
                    print(f"ID {id_} verified real image on verification image {img_p_n} and db image {img_db_n} with model {model_name} and distance of \
                        {result['distance']} and a threshold of {str(result['max_threshold_to_verify']).strip()}.")
                    log_to_file(f"ID {id_} verified real image on verification image {img_p_n} and db image {img_db_n} with model {model_name} and distance of\
                         {result['distance']} and a threshold of {str(result['max_threshold_to_verify']).strip()}.", "INFO")

                    if verified >= int(temp['VER_TOL']) or len(images_paths_normal):
                        print("Real verification reached tolerance. Verifying...")
                        log_to_file("Real verification reached tolerance. Verifying...", "SUCCESS")
                        return name, 200    

                for img_p_a in images_paths_aug:
                    for img_db_a in images_db_aug + images_db_normal:
                        result = DeepFace.verify(img_p_a, img_db_a, model_name = model_name, enforce_detection=False)

                    if result['verified']:
                        verified_aug += 1
                        print(f"ID {id_} verified augmented image on verification image {img_p_a} and db image {img_db_a} with model {model_name} and distance of \
                            {result['distance']} and a threshold of {str(result['max_threshold_to_verify']).strip()}.")
                        log_to_file(f"ID {id_} verified augmented image on verification image {img_p_a} and db image {img_db_a} with model {model_name} and distance of\
                            {result['distance']} and a threshold of {str(result['max_threshold_to_verify']).strip()}.", "INFO")

                    if verified_aug >= int(temp['VER_TOL_AUG']):
                        print("Augmentation verification reached tolerance. Verifying...")
                        log_to_file("Augmentation verification reached tolerance. Verifying...", "SUCCESS")
                        return name, 200                

    return False, 500