import unittest
import os
import shutil
from handler.admin.add_user import create_new_user_folder

class TestCreateNewUserFolder(unittest.TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.is_user_admin = False
        self.user_folder = "user_folder"

    def tearDown(self):
        # Clean up by removing the created directory after each test
        shutil.rmtree(f"{self.user_folder}/{self.username}", ignore_errors=True)

    def test_create_new_user_folder(self):
        result = create_new_user_folder(self.username, self.password, self.is_user_admin)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(f"{self.user_folder}/{self.username}"))
        self.assertTrue(os.path.exists(f"{self.user_folder}/{self.username}/user_info.txt"))
        self.assertTrue(os.path.exists(f"{self.user_folder}/{self.username}/{self.username}_annuaire.txt"))
        self.assertTrue(os.path.exists(f"{self.user_folder}/{self.username}/share_to_user.txt"))
        self.assertTrue(os.path.exists(f"{self.user_folder}/{self.username}/shared_by_me.txt"))

    def test_create_new_user_folder_already_exists(self):
        # Create the user folder
        result = create_new_user_folder(self.username, self.password, self.is_user_admin)
        self.assertTrue(result)

        # Attempt to create the user folder again
        result = create_new_user_folder(self.username, self.password, self.is_user_admin)
        self.assertEqual(result, "Couldn't create user because it already exists !")

    

if __name__ == "__main__":
    unittest.main()