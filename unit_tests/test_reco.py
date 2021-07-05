from params import *
import unittest
import os
from scripts.utils.log_to_file import open_log_file, close_log_file
from dotenv import dotenv_values
from shutil import rmtree
from main import *

temp = dotenv_values(".env")


class TestValidateEnv(unittest.TestCase):
    def test_aa_normal(self):
        code, name = main_reco(RECO_ID, TEST_IMGS, test_title="test_normal")

        self.assertEqual(code, 200)
        self.assertEqual(name, "chubak")

    def test_bb_hard_to_verify(self):
        code, name = main_reco(RECO_ID, HARD_TO_VERIFY, test_title="test_hard_to_verif")

        self.assertEqual(code, 134)
        self.assertEqual(name, "chubak")

    def test_cc_not_in_db(self):
        code, name = main_reco(RECO_ID, HARD_TO_VERIFY, test_title="test_hard_to_verify")

        self.assertEqual(code, 134)
        self.assertEqual(name, "chubak")

    def test_cc_not_in_db(self):
        code, name = main_reco(RECO_ID, IMG_NOT_IN_DB, test_title="test_not_in_db")

        self.assertTrue(code == 100 or code == 442)
        self.assertIsNone(name)
    
    def test_dd_bad_id(self):
        code, name = main_reco(RECO_ID + "24214", IMG_NOT_IN_DB, test_title="test_bad_id")

        self.assertEqual(code, 400)
        self.assertIsNone(name)

    
    def test_dd_empty_list(self):
        code, name = main_reco(RECO_ID, [], test_title="test_empty_list")

        self.assertEqual(code, 111)
        self.assertIsNone(name)

    def test_dd_non_existent_file(self):
        code, name = main_reco(RECO_ID, DB_NON_EXISTENT_MIX, test_title="test_non_existent_file")

        self.assertEqual(code, 159)
        self.assertIsNone(name)

    def test_dd_no_face(self):
        code, name = main_reco(RECO_ID, IMG_NO_FACE, test_title="test_no_face")

        self.assertEqual(code, 630)
        self.assertIsNone(name)

    def test_dd_face_spoof(self):
        code, name = main_reco(RECO_ID, IMGS_SPOOF, test_title="test_face_spoof")

        self.assertEqual(code, 630)
        self.assertIsNone(name)



if __name__ == "__main__":
    open_log_file()
    unittest.main()
    close_log_file()
