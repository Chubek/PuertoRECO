from deepface import DeepFace
from pprint import pprint
import pandas as pd
from dotenv import dotenv_values

temp = dotenv_values(".env")

def search_db(imgs):
    
    argmins = []

    for img in imgs:
        df = DeepFace.find(img_path = img, db_path = temp["DB_PATH"], model_name = temp["SELECTED_MODEL"], enforce_detection=False)
        argmins.append(df[temp["SELECTED_MODEL_COL"]].argmin())


    names_ids = [(f.split("_")[0], f.split("_")[1]) for f in argmins]

    return names_ids





