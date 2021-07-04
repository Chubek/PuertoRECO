import os
import sys
import inspect
import random

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

DB_IMGS = [r'I:\face_reco\test_imgs\chubak\chubak_1.png', r'I:\face_reco\test_imgs\chubak\chubak_2.png', r'I:\face_reco\test_imgs\chubak\chubak_3.png']
DB_NON_EXISTENT_MIX = [r'I:\face_reco\test_imgs\chubak\babasghoui.png', r'I:\face_reco\test_imgs\chubak\chubak_1.png']
TEST_IMGS = [r'I:\face_reco\test_imgs\chubak_test\chubak_test_2.png', r'I:\face_reco\test_imgs\chubak_test\chubak_test_3.png', \
    r'I:\face_reco\test_imgs\chubak_test\chubak_test.png']
MULTI_IMG_DB = [r'I:\face_reco\test_imgs\mamad_ammeymaryam.png', r'I:\face_reco\test_imgs\no_face.png']
MULTI_IMG_TEST = [r'I:\face_reco\test_imgs\chubak_test\multi_face.png']
IMG_NOT_IN_DB = [r'I:\face_reco\test_imgs\audrey\audrey_2.png']
HARD_TO_VERIFY = [r'I:\face_reco\test_imgs\chubak_test\harrd_to_verify.png']
ID = f"ID_00{random.randint(200, 2500)}"
NAME = "chubak"

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
"""