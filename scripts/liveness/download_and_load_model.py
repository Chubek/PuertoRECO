import gdown
from dotenv import dotenv_values
import os
import tensorflow.keras as keras
from scripts.utils.log_to_file import log_file, log_to_file

temp = dotenv_values(".env")

def down_load_model():
    if not os.path.exists(temp["MODEL_PATH"]):
        log_to_file(f"Model path {temp['MODEL_PATH']} does not exist. Creating...", "INFO")
        try:
            os.makedirs(temp["MODEL_PATH"])
            log_to_file(f"Path {temp['MODEL_PATH']} created.", "SUCCESS")
        except:
            log_to_file(f"Could not create path {temp['MODEL_PATH']}. Please check permissions.", "FAILURE")
            return False


    file_name = os.path.join(temp["MODEL_PATH"], temp["MODEL_NAME"])

    if not os.path.exists(file_name):
        url = f'{temp["MODEL_URL"]}'
        gdown.download(url, file_name, quiet=False)
        log_to_file(f"Model downloaded to {file_name}", "SUCCESS")


    return keras.models.load_model(file_name)