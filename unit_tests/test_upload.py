from params import *
import unittest
import os
from dotenv import dotenv_values
from shutil import rmtree
from main import *

temp = dotenv_values(".env")

class TestUpload(unittest.TestCase):
    def test_aa_normal_upload(self):
        """
        Test normal upload.
        """
        folder_path = os.path.join(temp['DB_PATH'], f"{NAME}-{ID}")

        if os.path.exists(folder_path):
            rmtree(folder_path, ignore_errors=True)
            log_to_file(f"Deleted folder {folder_path} for testing.", "INFO")


        message, message_pickle, rebuilt_db, res_main, res_aug, mysql_id = upload_to_db(DB_IMGS, ID, NAME, True, True, False, test_title="test_normal_upload")

        self.assertEqual(message, 800)
        self.assertIsInstance(mysql_id, int)
        self.assertIsInstance(message_pickle, dict)
        self.assertIsInstance(rebuilt_db, dict)
        self.assertIsInstance(res_main, list)
        self.assertIsInstance(res_aug, list)
        self.assertIn('result', message_pickle)
        self.assertIn('result', rebuilt_db)

    def test_bb_additional_upload_replace(self):
        """
        Test additional upload.
        """
        message, message_pickle, rebuilt_db, res_main, res_aug, mysql_id = upload_to_db(DB_IMGS, ID, NAME, False, False, True, test_title="test_additional_upload")

        self.assertEqual(message, 900)
        self.assertIsInstance(mysql_id, int)
        self.assertIsInstance(message_pickle, dict)
        self.assertIsInstance(rebuilt_db, dict)
        self.assertIsInstance(res_main, list)
        self.assertIsInstance(res_aug, list)
        self.assertIn('result', message_pickle)
        self.assertIn('result', rebuilt_db)
        self.assertEqual(message_pickle['result']['message'], "You haven't set to delete any of the pickle files. This will create issues in the database.\
         Unless that was your intention, please delete the pickle files.")
        self.assertEqual(rebuilt_db['result']['message'], "You have disabled delete_pickle so rebuild_db need not be enabled.")

    def test_bb_additional_upload(self):
        """
        Test additional upload.
        """
        message, message_pickle, rebuilt_db, res_main, res_aug, mysql_id = upload_to_db(DB_IMGS, ID, NAME, False, False, False, test_title="test_additional_upload")

        self.assertEqual(message, 850)
        self.assertIsInstance(mysql_id, int)
        self.assertIsInstance(message_pickle, dict)
        self.assertIsInstance(rebuilt_db, dict)
        self.assertIsInstance(res_main, list)
        self.assertIsInstance(res_aug, list)
        self.assertIn('result', message_pickle)
        self.assertIn('result', rebuilt_db)
        self.assertEqual(message_pickle['result']['message'], "You haven't set to delete any of the pickle files. This will create issues in the database.\
         Unless that was your intention, please delete the pickle files.")
        self.assertEqual(rebuilt_db['result']['message'], "You have disabled delete_pickle so rebuild_db need not be enabled.")

    def test_bb_additional_upload_needless(self):
        """
        Test additional upload.
        """
        message, message_pickle, rebuilt_db, res_main, res_aug, mysql_id = upload_to_db(DB_IMGS, ID_NEW, NAME, False, False, True, test_title="test_additional_upload")

        self.assertEqual(message, 838)
        self.assertIsInstance(mysql_id, int)
        self.assertIsInstance(message_pickle, dict)
        self.assertIsInstance(rebuilt_db, dict)
        self.assertIsInstance(res_main, list)
        self.assertIsInstance(res_aug, list)
        self.assertIn('result', message_pickle)
        self.assertIn('result', rebuilt_db)
        self.assertEqual(message_pickle['result']['message'], "You haven't set to delete any of the pickle files. This will create issues in the database.\
         Unless that was your intention, please delete the pickle files.")
        self.assertEqual(rebuilt_db['result']['message'], "You have disabled delete_pickle so rebuild_db need not be enabled.")

    def test_cc_multi_face_upload(self):
        """
        Test multi-face upload.
        """
        message, message_pickle, rebuilt_db, res_main, res_aug, _ = upload_to_db(MULTI_IMG_DB, ID, NAME, False, False, True, test_title="test_multi_face_upload")

        self.assertEqual(message, 152)
        self.assertIsNone(message_pickle)
        self.assertIsNone(rebuilt_db)
        self.assertIsNone(res_main)
        self.assertIsNone(res_aug)

    def test_dd_no_file(self):
        """
        Test none-existent file.
        """
        message, message_pickle, rebuilt_db, res_main, res_aug, _ = upload_to_db(DB_NON_EXISTENT_MIX, ID, NAME, False, False, True, test_title="test_no_file")

        self.assertEqual(message, 153)
        self.assertIsNone(message_pickle)
        self.assertIsNone(rebuilt_db)
        self.assertIsNone(res_main)
        self.assertIsNone(res_aug)

    def test_ee_empty_list(self):
        """
        Test empty list.
        """
        message, message_pickle, rebuilt_db, res_main, res_aug, _ = upload_to_db([], ID, NAME, False, False, True, test_title="test_empty_list")

        self.assertEqual(message, 111)
        self.assertIsNone(message_pickle)
        self.assertIsNone(rebuilt_db)
        self.assertIsNone(res_main)
        self.assertIsNone(res_aug)



if __name__ == "__main__":
    unittest.main()
    close_log_file()