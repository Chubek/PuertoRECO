from params import *
from main import *
import unittest
import os
from dotenv import dotenv_values
from shutil import rmtree
from scripts.utils.validate_env import *

temp = dotenv_values(".env")

class TestValidateEnv(unittest.TestCase):
    def test_aa_no_env(self):
        """
        Test that if .env doesn't exist
        """
        
        os.rename(env_file, env_file_renamed)

        res_reco, arr_reco, _ = main_reco(DB_IMGS, ID, test_title="test_no_env")
        arr_upload, res_upload, _, _, _, _ = upload_to_db(DB_IMGS, ID, NAME, True, True, test_title="test_no_env")

        self.assertEqual((res_reco, res_upload), (128, 128))
        self.assertIsInstance(arr_reco, list)
        self.assertIsInstance(arr_upload, list)
        self.assertEqual((len(arr_upload), len(arr_reco)), (2, 2))
        self.assertEqual((arr_upload[0][0], arr_upload[1][0]), ("Error reading .env: file doesn't exist.", "Error reading .env: file doesn't exist."))
        self.assertEqual((arr_reco[0][0], arr_reco[1][0]), ("Error reading .env: file doesn't exist.", "Error reading .env: file doesn't exist."))

        os.rename(env_file_renamed, env_file)

    def test_bb_prepare_env_empty(self):
        os.rename(env_file, env_file_renamed)

        f_env = open(env_file, 'w')
        f_env.close()

    def test_cc_no_keys(self):
        """
        Test that if keys in .env don't exist
        """       

        res_reco, arr_reco, _ = main_reco(DB_IMGS, ID, test_title="test_no_keys")
        arr_upload, res_upload, _, _, _, _ = upload_to_db(DB_IMGS, ID, NAME, True, True, test_title="test_no_env")

        self.assertEqual((res_reco, res_upload), (128, 128))
        self.assertIsInstance(arr_reco, list)
        self.assertIsInstance(arr_upload, list)
        self.assertEqual((len(arr_upload), len(arr_reco)), (2, 2))
        self.assertEqual((len(arr_upload[0]), len(arr_reco[0])), (12, 12))



    def test_dd_prepare_bad_keys(self):
        f_env = open(env_file, 'w')
        f_env.write(INVALID_ENV)
        f_env.close()

    def test_ee_env_errors(self):
        """
        Test that for errors in valid_env
        """    

        res_reco, arr_reco, _ = main_reco(DB_IMGS, ID, test_title="test_env_error")
        arr_upload, res_upload, _, _, _, _ = upload_to_db(DB_IMGS, ID, NAME, True, True, test_title="test_env_errors")

        self.assertEqual((res_reco, res_upload), (128, 128))
        self.assertIsInstance(arr_reco, list)
        self.assertIsInstance(arr_upload, list)
        self.assertEqual((len(arr_upload), len(arr_reco)), (2, 2))
        self.assertTrue(len(arr_upload[1]) >= 10)
        self.assertTrue(len(arr_reco[1]) >= 10)


    def test_ff_env_idregex(self):
        """
        Test that for id_regex check
        """
        val_res, not_in_env, env_errs = validate_id_regex(parentdir)
        
        self.assertEqual(val_res, False)
        self.assertListEqual(not_in_env, [])
        self.assertIn("Env file configured incorrectly: ID_REGEX is not a valid pattern.", env_errs)


    def test_gg_super_pass(self):
        """
        Test that for super_pass check
        """

        val_res, code, not_in_env, env_errs = validate_super_pass(parentdir)
        
        self.assertEqual(code, 175)
        self.assertEqual(val_res, False)
        self.assertListEqual(not_in_env, [])
        self.assertIn("Env file configured incorrectly: SUPER_PASS is not secure.", env_errs)


    def test_hh_mysql_val(self):
        """
        Test that for super_pass check
        """
        val_res, code, not_in_env, env_errs = validate_mysql_env(parentdir)
        
        self.assertEqual(code, 175)
        self.assertEqual(val_res, False)
        self.assertListEqual(not_in_env, [])
        self.assertEqual([f"Env file configured incorrectly: {fname} is either empty or does not match pattern, it can only be letter and underscore." \
            for fname in ["MONGO_COLL", "MONGO_DB"]], env_errs)

    def test_ii_rename_back(self):
        os.remove(env_file)
        os.rename(env_file_renamed, env_file)

if __name__ == "__main__":
    unittest.main()

    