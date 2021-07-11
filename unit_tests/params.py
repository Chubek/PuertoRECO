import os
import sys
import inspect
import gdown
import zipfile

file_name = os.path.join(os.getcwd(), "test_imgs.zip")

if not os.path.exists(file_name):
    url = 'https://drive.google.com/uc?id=1W9nSCmkPNr41MeDErwJuY_0rMKabsuak'
    gdown.download(url, file_name, quiet=False)

    if not os.path.exists(os.path.join(os.getcwd(), "test_imgs")):
        os.makedirs(os.path.join(os.getcwd(), "test_imgs"))

    with zipfile.ZipFile(file_name) as zf:
        zf.extractall(os.path.join(os.getcwd(), "test_imgs"))


make_path = lambda x: os.path.join(os.getcwd(), "test_imgs", *x)


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

env_file = os.path.join(parentdir, ".env")
env_file_renamed = os.path.join(parentdir, "temp_")

sys.path.insert(0, parentdir) 

DB_IMGS = [make_path(['rock_train', '1.jpg']), make_path(['rock_train', '2.png']), make_path(['rock_train', '3.jpg'])]
DB_NON_EXISTENT_MIX = [make_path(['doesntexist', 'doesntexist.jpg']), make_path(['rock_test', '1.jpg'])]
TEST_IMGS = [make_path(['rock_test', '1.jpg']), make_path(['rock_test', '2.png']), \
    make_path(['rock_test', '3.png'])]
MULTI_IMG_DB = [make_path(['imgs_mulit', 'diesel_rock.png']), make_path(['imgs_mulit', 'rock_diesel2.png'])]
IMG_NO_FACE = [make_path(['test_imgs', '1.png']), make_path(['test_imgs', '2.png'])]
MULTI_IMG_TEST = [make_path(['imgs_mulit', 'rock_wife.jpg'])]
IMG_NOT_IN_DB = [make_path(['angie_jolie', '1.jpg']), make_path(['angie_jolie', '2.png'])]
HARD_TO_VERIFY = [make_path(['rock_hard_verify', '1.jpg']),make_path(['rock_hard_verify', '2.png']), make_path(['rock_hard_verify', '2.png']),\
     make_path(['rock_hard_verify', 'unnamed.jpg'])]
IMGS_SPOOF = [make_path(['spoof_imgs', '1.jpg']), make_path(['spoof_imgs', '2.jpg']), make_path(['spoof_imgs', '3.jpg'])]
ID = "RECO_ID_99945"
RECO_ID = "RECO_ID_99945"
NAME = "rock"
ID_NEW = "RECO_ID_99935"
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