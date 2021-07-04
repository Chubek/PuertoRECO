from scripts.reco.log_to_file import log_to_file
from deepface import DeepFace
from pprint import pprint
import pandas as pd
from dotenv import dotenv_values
import os
from pathlib import Path

temp = dotenv_values(".env")

def search_db(imgs):
    print("Search DB starting...")
    log_to_file("Search in DB starting...", "Info")
    argmins = []

    for model_name, model_col in zip(((temp["SELECTED_MODEL_1"], temp["SELECTED_MODEL_2"], temp["SELECTED_MODEL_3"]), \
        (temp["SELECTED_MODEL_1_COL"], temp["SELECTED_MODEL_2_COL"], temp["SELECTED_MODEL_3_COL"]))):
        for img in imgs:
            df = DeepFace.find(img_path = img, db_path = temp["DB_PATH"], model_name = model_name, enforce_detection=False)
        
            if len(df) > 0:       
                index = df[model_col].argmin()
                argmins.append(df.loc[index, "identity"])
            else:
                continue


    if len(argmins) == 0:
        return False

    names_ids = [(str(Path(f).parts[-2]).split("-")[0], str(Path(f).parts[-2]).split("-")[1]) for f in argmins]
    print(f"Search in DB done. {len(names_ids)} names and IDs found.")
    log_to_file(f"Search in DB done. {len(names_ids)} names and IDs found.", "Success")
    return names_ids





