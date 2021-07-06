from re import S
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
        code, name, distance = main_reco(TEST_IMGS, RECO_ID, test_title="test_normal")

        self.assertEqual(code, 200)
        self.assertEqual(name, NAME)
        self.assertIsInstance(distance, float)

    def test_bb_hard_to_verify(self):
        code, name, distance = main_reco(HARD_TO_VERIFY, RECO_ID,  test_title="test_hard_to_verify", skip_verify=True)

        self.assertEqual(code, 134)
        self.assertEqual(name, NAME)
        self.assertIsInstance(distance, float)


    def test_cc_not_in_db(self):
        code, name, distance = main_reco(IMG_NOT_IN_DB, RECO_ID, test_title="test_not_in_db")

        self.assertTrue(code == 100 or code == 442 or code == 134)

    def test_dd_no_db_search(self):
        code, name, distance = main_reco(IMG_NOT_IN_DB, RECO_ID, test_title="test_no_db_search", skip_db_search=True)

        self.assertEqual(code, 500)
        self.assertTrue(name is None or not name)
        self.assertTrue(distance is None or not distance)

    def test_ee_both_true(self):
        code, name, distance = main_reco(IMG_NOT_IN_DB, RECO_ID, test_title="test_no_db_search", skip_db_search=True, skip_verify=True)

        self.assertEqual(code, 143)
        self.assertIsNone(name)
        self.assertIsNone(distance)
    
    def test_ff_bad_id(self):
        code, name, distance = main_reco(TEST_IMGS, RECO_ID + "24214", test_title="test_bad_id")

        self.assertEqual(code, 400)
        self.assertIsNone(name)
        self.assertIsNone(distance)

    
    def test_dd_empty_list(self):
        code, name, distance = main_reco([], RECO_ID, test_title="test_empty_list")

        self.assertEqual(code, 111)
        self.assertIsNone(name)
        self.assertIsNone(distance)

    def test_dd_non_existent_file(self):
        code, name, distance = main_reco(DB_NON_EXISTENT_MIX, RECO_ID, test_title="test_non_existent_file")

        self.assertEqual(code, 159)
        self.assertIsNone(name)
        self.assertIsNone(distance)

    def test_dd_no_face(self):
        code, name, distance = main_reco(IMG_NO_FACE, RECO_ID, test_title="test_no_face")

        self.assertEqual(code, 630)
        self.assertIsNone(name)
        self.assertIsNone(distance)

    def test_dd_face_spoof(self):
        code, name, distance = main_reco(IMGS_SPOOF, RECO_ID, test_title="test_face_spoof")

        self.assertEqual(code, 560)
        self.assertIsNone(name)
        self.assertIsNone(distance)


    def test_dd_face_multi(self):
        code, name, distance = main_reco(MULTI_IMG_TEST, RECO_ID, test_title="test_face_multi")

        self.assertTrue(code == 200 or code == 134)
        self.assertEqual(name, NAME)
        self.assertIsInstance(distance, float)



if __name__ == "__main__":
    open_log_file()
    unittest.main()
    close_log_file()
