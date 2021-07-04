import gdown
from dotenv import dotenv_values
import os
import tensorflow.keras as keras

temp = dotenv_values(".env")

def down_load_model():
    if not os.path.exists(temp["MODEL_PATH"]):
        os.makedirs(temp["MODEL_PATH"])

    file_name = os.path.join(temp["MODEL_PATH"], temp["MODEL_NAME"])

    if not os.path.exists(file_name):
        url = f'{temp["MODEL_URL"]}'
        gdown.download(url, file_name, quiet=False)

    return keras.models.load_model(file_name)