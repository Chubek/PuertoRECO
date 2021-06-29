from deepface import DeepFace
from pprint import pprint
import pandas as pd

models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
for model in models:
   df = DeepFace.find(img_path = r"test_imgs\IMG_20200809_191132.jpg", db_path = r"I:\face_reco\db", model_name = model, enforce_detection=False)
   df.to_csv(f"{model}.csv")




