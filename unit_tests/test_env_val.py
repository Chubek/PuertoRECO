from params import *
from main import *
import unittest
import os
from scripts.utils.log_to_file import open_log_file, close_log_file
from dotenv import dotenv_values
from shutil import rmtree

temp = dotenv_values(".env")

class TestValidateEnv(unittest.TestCase):
    def test_no_env(self):
        """
        Test that if .env doesn't exist
        """
        env_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env")
        env_file_renamed = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp_")
        os.rename(env_file, env_file_renamed)

        arr_reco, res_reco = main_reco(DB_IMGS, ID, test_title="test_no_env")
        arr_upload, res_upload, _, _, _, _ = upload_to_db(DB_IMGS, ID, NAME, True, True, test_title="test_no_env")

        self.assertEqual((res_reco, res_upload), (128, 128))
        self.assertIsInstance(arr_reco, list)
        self.assertIsInstance(arr_upload, list)
        self.assertEqual((len(arr_upload), len(arr_reco)), (2, 2))
        self.assertEqual((arr_upload[0][0], arr_upload[1][0]), ("Error reading .env: file doesn't exist.", "Error reading .env: file doesn't exist."))
        self.assertEqual((arr_reco[0][0], arr_reco[1][0]), ("Error reading .env: file doesn't exist.", "Error reading .env: file doesn't exist."))

        os.rename(env_file_renamed, env_file)

    def test_no_keys(self):
        """
        Test that if keys in .env don't exist
        """
        env_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env")
        env_file_renamed = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp_")
        os.rename(env_file, env_file_renamed)

        f_env = open(env_file, 'w')
        f_env.close()

        arr_reco, res_reco = main_reco(DB_IMGS, ID, test_title="test_no_keys")
        arr_upload, res_upload, _, _, _, _ = upload_to_db(DB_IMGS, ID, NAME, True, True, test_title="test_no_env")

        self.assertEqual((res_reco, res_upload), (128, 128))
        self.assertIsInstance(arr_reco, list)
        self.assertIsInstance(arr_upload, list)
        self.assertEqual((len(arr_upload), len(arr_reco)), (2, 2))
        self.assertEqual((len(arr_upload[0]), len(arr_reco[0])), (16, 16))

        os.remove(env_file)
        os.rename(env_file_renamed, env_file)

    def test_env_errors(self):
        """
        Test that for errors in valid_env
        """
        env_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env")
        env_file_renamed = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp_")
        os.rename(env_file, env_file_renamed)

        f_env = open(env_file, 'w')
        f_env.write(INVALID_ENV)
        f_env.close()

        arr_reco, res_reco = main_reco(DB_IMGS, ID, test_title="test_env_error")
        arr_upload, res_upload, _, _, _, _ = upload_to_db(DB_IMGS, ID, NAME, True, True, test_title="test_env_errors")

        self.assertEqual((res_reco, res_upload), (128, 128))
        self.assertIsInstance(arr_reco, list)
        self.assertIsInstance(arr_upload, list)
        self.assertEqual((len(arr_upload), len(arr_reco)), (2, 2))
        self.assertTrue(len(arr_upload[1]) >= 10)
        self.assertTrue(len(arr_reco[1]) >= 10)

        os.remove(env_file)
        os.rename(env_file_renamed, env_file)

if __name__ == "__main__":
    open_log_file()
    unittest.main()
    close_log_file()

    