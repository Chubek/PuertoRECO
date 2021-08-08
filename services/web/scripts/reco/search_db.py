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
        log_to_file(f"Model {model_name} selected.", "INFO")
        for img in imgs:
            log_to_file(f"Searching for image {img} in the database.", "INFO")
            df = DeepFace.find(img_path = img, db_path = temp["DB_PATH"], model_name = model_name, enforce_detection=False)
        
            if len(df) > 0:                 
                index = df[f"{model_name}_{temp['SIM_FUNC']}"].argmin()
                identity = df.loc[index, "identity"]
                distance = df.loc[index, f"{model_name}_{temp['SIM_FUNC']}"]
                argmins.append((identity, distance))
                log_to_file(f"Got an identity of {identity} and a distance of {distance}.", "INFO")
            else:
                continue
    
    log_to_file(f"Got {len(argmins)} argmin values.", "INFO")

    if len(argmins) == 0:
        return []

    names_ids_distances = [(str(Path(f[0]).parts[-3]).split("-")[0], str(Path(f[0]).parts[-3]).split("-")[1], f[1]) for f in argmins]
    log_to_file(f"Search in DB done. {len(names_ids_distances)} names, IDs and distances found.", "SUCCESS")
    
    return names_ids_distances





