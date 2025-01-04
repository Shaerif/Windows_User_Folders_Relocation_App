
import unittest
from folder_relacator import UserFolderRelocator

class TestUserFolderRelocator(unittest.TestCase):
    def setUp(self):
        self.relocator = UserFolderRelocator(dry_run=True)

    def test_is_admin(self):
        # Test administrative privileges check
        self.assertFalse(self.relocator.is_admin())

    def test_validate_path_success(self):
        # Test path validation with a valid path
        valid, message = self.relocator.validate_path("C:/Valid/Path")
        self.assertTrue(valid)
        self.assertEqual(message, "Path validation successful")

    def test_validate_path_invalid_drive(self):
        # Test path validation with an invalid drive
        valid, message = self.relocator.validate_path("Z:/Invalid/Path")
        self.assertFalse(valid)
        self.assertIn("Invalid drive specification", message)

    def test_backup_registry(self):
        # Test registry backup functionality
        result = self.relocator.backup_registry()
        self.assertTrue(result)

    def test_update_registry(self):
        # Test registry update functionality
        result = self.relocator.update_registry("Documents", "D:/Users/TestUser/Documents")
        self.assertTrue(result)

    def test_move_folder_contents(self):
        # Test moving folder contents
        result = self.relocator.move_folder_contents(
            "C:/Users/TestUser/Documents",
            "D:/Users/TestUser/Documents",
            skip_checksum=False,
            delete_files=False
        )
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()