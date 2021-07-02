from deepface import DeepFace
from pprint import pprint
import pandas as pd

df = DeepFace.find(img_path = r"test_imgs\IMG_20200809_191132.jpg", db_path = r"I:\face_reco\db", model_name = "Facenet", enforce_detection=False)
df.to_csv(f"facenet.csv")




