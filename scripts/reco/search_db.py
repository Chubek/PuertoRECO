from scripts.utils.log_to_file import log_to_file
from deepface import DeepFace
from pprint import pprint
import pandas as pd
from dotenv import dotenv_values
import os
from pathlib import Path

temp = dotenv_values(".env")

def search_db(imgs):
    log_to_file("Search in DB starting...", "INFO")
    argmins = []

    for model_name in  [m.strip() for m in temp["SELECTED_MODELS"].split(',')]:
        for img in imgs:
            df = DeepFace.find(img_path = img, db_path = temp["DB_PATH"], model_name = model_name, enforce_detection=False)
        
            if len(df) > 0:       
                index = df[f"{model_name}_{temp['SIM_FUNC']}"].argmin()
                argmins.append(df.loc[index, "identity"])
            else:
                continue


    if len(argmins) == 0:
        return []

    names_ids = [(str(Path(f).parts[-2]).split("-")[0], str(Path(f).parts[-2]).split("-")[1]) for f in argmins]
    log_to_file(f"Search in DB done. {len(names_ids)} names and IDs found.", "SUCCESS")
    
    return names_ids





