import unittest
from unittest.mock import patch, MagicMock
from folder_relacator import UserFolderRelocator

class TestUserFolderRelocatorIntegration(unittest.TestCase):
    def setUp(self):
        self.relocator = UserFolderRelocator(dry_run=True)

    @patch('folder_relacator.UserFolderRelocator.validate_path')
    @patch('folder_relacator.UserFolderRelocator.backup_registry')
    @patch('folder_relacator.UserFolderRelocator.move_folder_contents')
    @patch('folder_relacator.UserFolderRelocator.update_registry')
    def test_relocate_folder_success(self, mock_update_registry, mock_move_contents, mock_backup, mock_validate):
        # Mock the methods to simulate successful relocation
        mock_validate.return_value = (True, "Path validation successful")
        mock_backup.return_value = True
        mock_move_contents.return_value = True
        mock_update_registry.return_value = True

        result = self.relocator.relocate_folder('Documents', 'D:/Users/TestUser/Documents')
        self.assertTrue(result)
        mock_validate.assert_called_once_with('D:/Users/TestUser/Documents')
        mock_backup.assert_called_once()
        mock_move_contents.assert_called_once()
        mock_update_registry.assert_called_once()

    @patch('folder_relacator.UserFolderRelocator.validate_path')
    def test_relocate_folder_invalid_path(self, mock_validate):
        # Simulate invalid path
        mock_validate.return_value = (False, "Invalid drive specification")
        result = self.relocator.relocate_folder('Documents', 'Z:/Invalid/Path')
        self.assertFalse(result)

    @patch('folder_relacator.UserFolderRelocator.validate_path')
    @patch('folder_relacator.UserFolderRelocator.backup_registry')
    def test_relocate_folder_backup_failure(self, mock_backup, mock_validate):
        # Simulate backup failure
        mock_validate.return_value = (True, "Path validation successful")
        mock_backup.return_value = False

        result = self.relocator.relocate_folder('Documents', 'D:/Users/TestUser/Documents')
        self.assertFalse(result)
        mock_backup.assert_called_once()

    @patch('folder_relacator.UserFolderRelocator.validate_path')
    @patch('folder_relacator.UserFolderRelocator.backup_registry')
    @patch('folder_relacator.UserFolderRelocator.move_folder_contents')
    def test_relocate_folder_move_failure(self, mock_move_contents, mock_backup, mock_validate):
        # Simulate move failure
        mock_validate.return_value = (True, "Path validation successful")
        mock_backup.return_value = True
        mock_move_contents.return_value = False

        result = self.relocator.relocate_folder('Documents', 'D:/Users/TestUser/Documents')
        self.assertFalse(result)
        mock_move_contents.assert_called_once()

    # ...additional integration tests...

if __name__ == '__main__':
    unittest.main()