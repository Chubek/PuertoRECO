import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

env_file = os.path.join(parentdir, ".env")
env_file_renamed = os.path.join(parentdir, "temp_")

sys.path.insert(0, parentdir) 

DB_IMGS = [r'I:\face_reco\test_imgs\rock_train\1.jpg', r'I:\face_reco\test_imgs\rock_train\2.png', r'I:\face_reco\test_imgs\rock_train\3.jpg']
DB_NON_EXISTENT_MIX = [r'I:\face_reco\test_imgs\chubak\babasghoui.png', r'I:\face_reco\test_imgs\rock_test\1.jpg']
TEST_IMGS = [r'I:\face_reco\test_imgs\rock_test\1.jpg', r'I:\face_reco\test_imgs\rock_test\2.png', \
    r'I:\face_reco\test_imgs\rock_test\3.png']
MULTI_IMG_DB = [r'I:\face_reco\test_imgs\imgs_mulit\diesel_rock.png', r'I:\face_reco\test_imgs\imgs_mulit\rock_diesel2.png']
IMG_NO_FACE = [r'I:\face_reco\test_imgs\image_with_no_face\1.png', r'I:\face_reco\test_imgs\image_with_no_face\2.png']
MULTI_IMG_TEST = [r'I:\face_reco\test_imgs\imgs_mulit\rock_wife.jpg']
IMG_NOT_IN_DB = [r'I:\face_reco\test_imgs\angie_jolie\1.jpg', r'I:\face_reco\test_imgs\angie_jolie\2.png']
HARD_TO_VERIFY = [r'I:\face_reco\test_imgs\rock_hard_verify\1.jpg', r'I:\face_reco\test_imgs\rock_hard_verify\2.png', r'I:\face_reco\test_imgs\rock_hard_verify\2.png',\
     r'I:\face_reco\test_imgs\rock_hard_verify\unnamed.jpg']
IMGS_SPOOF = [r'I:\face_reco\test_imgs\spoof_imgs\1.jpg', r'I:\face_reco\test_imgs\spoof_imgs\2.jpg', r'I:\face_reco\test_imgs\spoof_imgs\3.jpg']
PICKLED_REQ = os.path.join(os.getcwd(), "unit_tests", "necessary_files", "req_files.pickle")
TEMP_PATH = os.path.join(os.getcwd(), "unit_tests", "necessary_files", "temp")
ID = "RECO_ID_9990"
RECO_ID = "RECO_ID_9990"
NAME = "rock"

INVALID_ENV = """
MODEL_PATH=bin?model
MODEL_URL=drive.google.com/uc?id=1G2RQ3rXtw6RmTjyBFlJEnd5UNo7zkRWX
MONGO_URI=mongodb+srv://cherry-chubak:R3n0_Nevada@cluster0.if2ry.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
MODEL_NAME=liveness_best
MONGO_DB=reco_d/*-=b
MONGO_COLL=reco_col&`13=l
DB_PATH=I:lllface_reco--db
TARGET_WIDTH=24f
TARGET_HEIGHT=22ss4
SELECTED_MODELS=Facenet|ArcFace|"VGG-Face
ID_REGEX=[0-9]++
NUM_AUG=4y
SIM_FUNC=cosinus
LOG_LOC=I:\\face_reco\\faceapp
VER_TOL=28u
VER_TOL_AUG=2u
SUPER_PASS=badpass
"""