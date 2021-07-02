from deepface import DeepFace
import glob
from dotenv import dotenv_values

temp = dotenv_values(".env")

def verify_face(mongo_client, id, img_paths):
    row = mongo_client.find_one({"reco_id": id})

    if len(row) < 1:
        return False, 300

    images = glob.glob(f"{row[0]['db_path']}/*.png")

    results = []

    for img_ver in img_paths:
        for img_db in images:
            result = DeepFace.verify(img_ver, img_db, model_name = temp["SELECTED_MODEL"])

            results.append(result)


    for res in results:
        if res["verified"]:
            return True, 200
            break
        else:
            return False, 400