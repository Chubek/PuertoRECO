from scripts.reco.search_db import search_db
from scripts.reco.verify_faces import verify_face
from scripts.reco.upload_to_db import main_upload, save_imgs, verify_image
from scripts.reco.prepare_img import prepare_img
from scripts import *
import pymongo
from scripts.liveness.predict_label import *
from scripts.liveness.img_op import *
from scripts.liveness.detect_faces import *
from scripts.liveness.save_final import *
from dotenv import dotenv_values
import functools
import operator

temp = dotenv_values(".env")
dbclient = pymongo.MongoClient(temp["MONGO_URI"])





def main_reco(img_paths, id_):
    print(f"Starting recognition process with {len(img_paths)} images...")
    face_img_paths = []

    if len(img_paths) == 0:
        return 111

    prepared_imgs = [prepare_img(img) for img in img_paths]

    face_img_paths.extend(prepared_imgs)

    if len(face_img_paths) == 0:
        return 630

    face_img_paths = functools.reduce(operator.iconcat, face_img_paths, [])

    print(f"A total of {len(face_img_paths)} real and augmented images are ready for verification.")

    liveness_pred = predict_spoof([f for f in face_img_paths if "AUGMENTED" not in f])

    len_spoof = len([label for label, _ in liveness_pred if label == 1])

    print(f"Found {len_spoof} spoof images.")

    if len_spoof > 1:
        print("All of the images were spoof. Aborting...")
        return 560
    
    status, message = verify_face(dbclient, id_, face_img_paths)

    if status:
        return message
    else:
        if message == 400:
            return message
        else:
            print("Image unverified... searching db...")
            ids_names = search_db(face_img_paths)
            print(f"Found ids and names: {ids_names}")
            if ids_names == True:
                for id__, _ in ids_names:
                    if id__ == id_:
                        print("ID matched.")
                        return 134
                    else:
                        print("ID didn't match.")
                        return 100
            else:
                return 442


def upload_to_db(imgs_path, id_, name, delete_pickle, rebuild_db):
    print(f"Starting upload to db for id {id_} and name {name}")
    if len(imgs_path) == 0:
        return "Length of imgs list was 0", None, None, None, None, None
    
    result, message, message_pickle, rebuilt_db, res_main, res_aug = main_upload(dbclient, imgs_path, id_, name, delete_pickle, rebuild_db)

    print("Upload to db done.")

    return result, message, message_pickle, rebuilt_db, res_main, res_aug

#print(upload_to_db([r"I:\face_reco\test_imgs\elhaam\elhaam_1.png", r"I:\face_reco\test_imgs\elhaam\elhaam_2.png", r"I:\face_reco\test_imgs\elhaam\elhaam_3.png"], 'RECO_ID_001', "elhaam_rr", True, True))
print(main_reco([r"I:\face_reco\test_imgs\elhaam.png", r"I:\face_reco\test_imgs\elham_test2.png", r"I:\face_reco\test_imgs\elhaam_test_3.png"], "RECO_ID_001"))
    
