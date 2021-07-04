from deepface import DeepFace
import glob
from dotenv import dotenv_values
import pymongo
import platform
import log_to_file

temp = dotenv_values(".env")

def verify_face(mongo_client, id_, img_paths):
    print("Files to verify: " + str(img_paths))
    log_to_file("Files to verify: " + str(img_paths), "Info")
    db = mongo_client[temp["MONGO_DB"]]
    coll= db[temp["MONGO_COLL"]]

    row = coll.find_one({"reco_id": id_})

    if row is None:
        print("Found didn't find the ID in the database.")
        log_to_file("Files to verify: " + str(img_paths), "Error")
        return False, 400

    if platform.system() == "Windows":
        images = glob.glob(row['db_path'] + r"\*.png")
    else:
        images = glob.glob(f"{row['db_path']}/*.png")

    print("Images found in db: " + str(images))
    log_to_file("Images found in db: " + str(images), "Info")
    
    for model_name in (temp["SELECTED_MODEL_1"], temp["SELECTED_MODEL_2"], temp["SELECTED_MODEL_3"]):
        print(f"Trying model {model_name}")
        for img_ver in img_paths:
            for img_db in images:
                result = DeepFace.verify(img_ver, img_db, model_name = model_name, enforce_detection=False)

                if result['verified'] == True:
                    print(f"Verified on verification image {img_ver} and db image {img_db} with model {model_name}.")
                    log_to_file(f"Verified on verification image {img_ver} and db image {img_db} with model {model_name}.", "Success")
                    return True, 200
                    break
                else:
                    continue



    return False, 500