from main import *
import unittest
import os
from scripts.utils.log_to_file import open_log_file, close_log_file
from dotenv import dotenv_values
from shutil import rmtree
from unit_tests.params import *

temp = dotenv_values(".env")

class TestUpload(unittest.TestCase):
    def test_normal_upload(self):
        """
        Test normal upload.
        """
        folder_path = os.path.join(temp['DB_PATH'], f"{NAME}-{ID}")

        if os.path.exists(folder_path):
            rmtree(folder_path, ignore_errors=True)


        result, message, message_pickle, rebuilt_db, res_main, res_aug = upload_to_db(DB_IMGS, ID, NAME, True, True, test_title="test_normal_upload")

        self.assertEqual(message, 800)
        self.assertIsInstance(result, str)
        self.assertIsInstance(message_pickle, dict)
        self.assertIsInstance(rebuilt_db, dict)
        self.assertIsInstance(res_main, list)
        self.assertIsInstance(res_aug, list)
        self.assertIn('result', message_pickle)
        self.assertIn('result', rebuilt_db)

    def test_additional_upload(self):
        """
        Test additional upload.
        """
        result, message, message_pickle, rebuilt_db, res_main, res_aug = upload_to_db(DB_IMGS, ID, NAME, False, False, test_title="test_additional_upload")

        self.assertEqual(message, 900)
        self.assertEqual(f"{ID} already exists in DB, updated images.", result)
        self.assertIsInstance(result, str)
        self.assertIsInstance(message_pickle, dict)
        self.assertIsInstance(rebuilt_db, dict)
        self.assertIsInstance(res_main, list)
        self.assertIsInstance(res_aug, list)
        self.assertIn('result', message_pickle)
        self.assertIn('result', rebuilt_db)
        self.assertEqual(message_pickle['result']['message'], "You haven't set to delete any of the pickle files. This will create issues in the database.\
         Unless that was your intention, please delete the pickle files.")
        self.assertEqual(rebuilt_db['result']['message'], "You have disabled delete_pickle so rebuild_db need not be enabled.")

    def test_multi_face_upload(self):
        """
        Test multi-face upload.
        """
        result, message, message_pickle, rebuilt_db, res_main, res_aug = upload_to_db(MULTI_IMG_DB, ID, NAME, False, False, test_title="test_multi_face_upload")

        self.assertEqual(message, 150)
        self.assertEqual(f"Could not detect a face in any of the images or all contained more than one face", result)
        self.assertIsNone(message_pickle)
        self.assertIsNone(rebuilt_db)
        self.assertIsNone(res_main)
        self.assertIsNone(res_aug)

    def test_no_file(self):
        """
        Test none-existent file.
        """
        result, message, message_pickle, rebuilt_db, res_main, res_aug = upload_to_db(DB_NON_EXISTENT_MIX, ID, NAME, False, False, test_title="test_no_file")

        self.assertEqual(message, 987)
        self.assertEqual(f"File {DB_NON_EXISTENT_MIX[0]} doesn't exist.", result)
        self.assertIsNone(message_pickle)
        self.assertIsNone(rebuilt_db)
        self.assertIsNone(res_main)
        self.assertIsNone(res_aug)

    def test_empty_list(self):
        """
        Test empty list.
        """
        result, message, message_pickle, rebuilt_db, res_main, res_aug = upload_to_db([], ID, NAME, False, False)

        self.assertEqual(message, 981)
        self.assertEqual("Length of imgs list was 0", result)
        self.assertIsNone(message_pickle)
        self.assertIsNone(rebuilt_db)
        self.assertIsNone(res_main)
        self.assertIsNone(res_aug)



if __name__ == "__main__":
    open_log_file()
    unittest.main()
    close_log_file()

    