"""
Windows User Folders Relocation Tool
Generic implementation for Windows systems with wxPython GUI support
"""

import os
import sys
import shutil
import winreg
import ctypes
import logging
from pathlib import Path
import json
from datetime import datetime
import win32com.client
import argparse
import wx
import wx.lib.agw.pygauge as PG
import platform
import traceback

def parse_arguments():
    # This function parses command-line arguments and returns an object
    # containing user-specified parameters like --target, --folders, etc.
    parser = argparse.ArgumentParser(description='Windows User Folders Relocation Tool')
    parser.add_argument('--target', type=str,
                      help='Target base directory for folder relocation')
    parser.add_argument('--folders', type=str,
                      help='Comma-separated list of folders to relocate (default: all)')
    parser.add_argument('--dry-run', action='store_true',
                      help='Perform a test run without making changes')
    parser.add_argument('--no-backup', action='store_true',
                      help='Skip registry backup (not recommended)')
    parser.add_argument('--log-file', type=str,
                      help='Specify a custom log file location')
    return parser.parse_args()

def choose_drive():
    # Lists all valid drives on the system and prompts the user to choose one.
    # Terminates the script if the choice is invalid.
    drives = [f"{d}:\\" for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f"{d}:\\")]
    print("Available drives:")
    for i, drive in enumerate(drives):
        print(f"{i + 1}. {drive}")
    
    choice = int(input("Choose the drive number to relocate user folders: ")) - 1
    if 0 <= choice < len(drives):
        return drives[choice]
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

class UserFolderRelocator:
    # The main class handling the relocation logic.
    # It stores options like dry_run, skip_backup, and log_file.
    # Also contains methods for verifying paths, moving folders,
    # updating the registry, and more.
    """
    A class to handle the relocation of Windows user folders.
    Supports moving Documents, Downloads, Pictures, Music, Videos, and Desktop folders
    while updating necessary registry entries and maintaining system compatibility.
    """

    def __init__(self, dry_run=False, skip_backup=False, log_file=None, gui=None, overwrite_files=False, overwrite_folders=False, overwrite_all=False):
        self.dry_run = dry_run
        self.skip_backup = skip_backup
        self.gui = gui
        
        self.overwrite_files = overwrite_files
        self.overwrite_folders = overwrite_folders
        self.overwrite_all = overwrite_all
        
        # Dynamic paths based on the user's home directory
        self.user_home = Path(os.path.expanduser("~"))
        log_dir = self.user_home / "WindowsUserFoldersRelocation" / "logs"
        backup_dir = self.user_home / "WindowsUserFoldersRelocation" / "backups"
        log_dir.mkdir(parents=True, exist_ok=True)
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Set the log file path
        self.log_file = log_file or log_dir / f"folder_relocation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        self.known_folders = {
            'Documents': {'id': 'Personal', 'guid': '{F42EE2D3-909F-4907-8871-4C22FC0BF756}'},
            'Downloads': {'id': '{374DE290-123F-4565-9164-39C4925E467B}', 'guid': '{374DE290-123F-4565-9164-39C4925E467B}'},
            'Pictures': {'id': 'My Pictures', 'guid': '{33E28130-4E1E-4676-835A-98395C3BC3BB}'},
            'Music': {'id': 'My Music', 'guid': '{4BD8D571-6D19-48D3-BE97-422220080E43}'},
            'Videos': {'id': 'My Video', 'guid': '{18989B1D-99B5-455B-841C-AB7C74E4DDFC}'},
            'Desktop': {'id': 'Desktop', 'guid': '{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}'},
            'AppData': {'id': 'AppData', 'guid': '{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}'},
            'Temp Folders': {'id': 'Temp', 'guid': '{AF9CD9E0-4F9B-4FC4-A2E0-3F4CA754252E}'},
            'OneDrive': {'id': 'OneDrive', 'guid': '{018D5C66-4533-4307-9B53-224DE2ED1FE6}'},
            'Public Folders': {'id': 'Public', 'guid': '{DFDF76A2-C830-4D7E-AA17-262CAA8955E5}'}
        }
        
        self.setup_logging()
        self.report = {
            "success": False,
            "moved_files": [],
            "total_size": 0,
            "errors": []
        }
        
    def setup_logging(self):
        # Configures logging to both a file and console with detailed format
        logging.basicConfig(
            level=logging.DEBUG,  # Set to DEBUG for detailed logs
            format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging setup complete.")
        self.logger.debug("Logging initialized with DEBUG level.")
    
    def is_admin(self):
        self.logger.debug("Checking for administrative privileges.")
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            self.logger.debug(f"Administrative privileges: {is_admin}")
            return is_admin
        except Exception as e:
            self.logger.error("Failed to check administrative privileges.")
            self.logger.error(traceback.format_exc())
            return False
    
    def get_user_shell_folders_path(self):
        # Returns the registry path holding user folder locations.
        # This is the location we need to update for folder relocation.
        return r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"

    def validate_path(self, new_path):
        # Ensures the new destination path is valid, accessible, and
        # meets safe relocation criteria such as available disk space.
        """
        Validates the new path for folder relocation.
        
        Args:
            new_path (str): The target path for folder relocation
            
        Returns:
            tuple: (bool, str) - Success status and validation message
        """
        try:
            path = Path(new_path).resolve()
            
            # Additional checks for system-protected paths
            system_drive = os.environ.get('SystemDrive', 'C:')
            if str(path).startswith(f"{system_drive}\\Windows"):
                return False, "Cannot relocate to Windows system directories"

            # Check if drive exists and is local
            if not path.drive:
                return False, "Invalid drive specification"
            
            # Check if drive exists
            if not path.exists():
                try:
                    path.mkdir(parents=True)
                except Exception as e:
                    return False, f"Cannot create directory: {str(e)}"
            
            # Check available space (minimum 5GB)
            free_space = shutil.disk_usage(path.drive).free
            if free_space < (5 * 1024 * 1024 * 1024):  # 5GB in bytes
                return False, "Insufficient disk space (minimum 5GB required)"
            
            return True, "Path validation successful"
        except Exception as e:
            return False, f"Path validation failed: {str(e)}"

    def backup_registry(self):
        self.logger.debug("Starting registry backup process.")
        # Creates a .reg backup for the registry entries before we make changes.
        # This is critical for rollback in case of unexpected issues.
        """
        Creates a backup of relevant registry keys before modification.
        Exports the User Shell Folders registry key to a timestamped .reg file.
        
        Returns:
            bool: True if backup successful, False otherwise
        """
        if self.skip_backup:
            logging.info("Skipping registry backup as per user request")
            return True

        try:
            backup_file = f"backups/registry_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.reg"
            if os.path.exists(backup_file):
                if self.gui:
                    overwrite = wx.MessageBox(f"File {backup_file} already exists. Overwrite?", "Confirm", wx.YES_NO | wx.ICON_QUESTION)
                    if overwrite != wx.YES:
                        return False
                else:
                    overwrite = input(f"File {backup_file} already exists. Overwrite (Yes/No)? ")
                    if overwrite.lower() != 'yes':
                        return False

            os.system(f'reg export "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders" "{backup_file}" /y')
            self.logger.info(f"Registry backup created: {backup_file}")
            self.logger.debug("Registry backup process completed successfully.")
            return True
        except Exception as e:
            self.logger.error("Registry backup failed.")
            self.logger.error(traceback.format_exc())
            return False
    
    def update_registry(self, folder_name, new_path):
        self.logger.debug(f"Updating registry for folder: {folder_name} to new path: {new_path}")
        # Applies changes to the Windows registry to point a known folder
        # (Documents, Downloads, etc.) to the newly relocated path.
        """
        Updates the Windows registry to point to the new folder location.
        
        Args:
            folder_name (str): Name of the folder to update
            new_path (str): New path for the folder
            
        Returns:
            bool: True if registry update successful, False otherwise
        """
        if self.dry_run:
            logging.info(f"DRY RUN: Would update registry for {folder_name} to {new_path}")
            return True

        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.get_user_shell_folders_path(),
                0, winreg.KEY_SET_VALUE
            )
            
            winreg.SetValueEx(
                key,
                self.known_folders[folder_name]['id'],
                0,
                winreg.REG_EXPAND_SZ,
                str(new_path)
            )
            
            winreg.CloseKey(key)
            self.logger.info(f"Registry updated for {folder_name}: {new_path}")
            return True
        except Exception as e:
            self.logger.error(f"Registry update failed for {folder_name}.")
            self.logger.error(traceback.format_exc())
            return False
    
    def move_folder_contents(self, old_path, new_path, skip_checksum, delete_files):
        self.logger.debug(f"Moving contents from {old_path} to {new_path}. Skip checksum: {skip_checksum}, Delete files: {delete_files}")
        # Copies the existing user data to the target folder location.
        # Displays progress, verifies file integrity, and creates a
        # junction point to maintain compatibility with system references.
        """
        Safely moves folder contents to the new location with progress tracking
        and verification. Creates a junction point at the old location.
        
        Args:
            old_path (Path): Original folder path
            new_path (Path): Destination folder path
            skip_checksum (bool): Skip checksum validation
            delete_files (bool): Delete files after relocation
            
        Returns:
            bool: True if move successful, False otherwise
        """
        if self.dry_run:
            logging.info(f"DRY RUN: Would move {old_path} to {new_path}")
            return True

        try:
            old_path = Path(old_path)
            new_path = Path(new_path)
            
            # Create destination if it doesn't exist
            new_path.mkdir(parents=True, exist_ok=True)
            
            # Check if target folder already exists
            if new_path.exists():
                if self.overwrite_all:
                    try:
                        shutil.rmtree(new_path)
                        logging.info(f"Deleted existing target folder: {new_path}")
                    except Exception as e:
                        logging.error(f"Failed to delete existing folder: {str(e)}")
                        self.report["errors"].append(f"Failed to delete existing folder: {str(e)}")
                        return False
                else:
                    # For CLI, prompt the user
                    if not self.gui:
                        while True:
                            user_input = input(f"The target folder '{new_path}' already exists. Overwrite? (y/n): ").strip().lower()
                            if user_input == 'y':
                                try:
                                    shutil.rmtree(new_path)
                                    logging.info(f"Deleted existing target folder: {new_path}")
                                except Exception as e:
                                    logging.error(f"Failed to delete existing folder: {str(e)}")
                                    self.report["errors"].append(f"Failed to delete existing folder: {str(e)}")
                                    return False
                                break
                            elif user_input == 'n':
                                logging.info(f"Skipped relocating folder: {new_path}")
                                self.report["errors"].append(f"Skipped relocating folder: {new_path}")
                                return False

            # Move the folder contents
            try:
                shutil.move(str(old_path), str(new_path))
                logging.info(f"Moved folder contents: {old_path} -> {new_path}")
                self.report["moved_files"].append(str(old_path))
            except Exception as e:
                logging.error(f"Moving folder contents failed: {str(e)}")
                logging.error(traceback.format_exc())
                self.report["errors"].append(str(e))
                return False
            
            # Verify total file count if not skipping checksum
            if not skip_checksum:
                original_file_count = sum(1 for _ in old_path.rglob('*') if _.is_file())
                new_file_count = sum(1 for _ in new_path.rglob('*') if _.is_file())
                logging.error(f"Failed to create junction point for {old_path}")
                self.report["errors"].append(f"Failed to create junction point for {old_path}")
                return False
            logging.info(f"Junction created for {old_path} <<===>> {new_path}")
            
            # Optionally delete original folder if required
            if delete_files:
                try:
                    shutil.rmtree(old_path)
                    logging.info(f"Deleted original folder: {old_path}")
                except Exception as e:
                    logging.error(f"Failed to delete original folder: {str(e)}")
                    self.report["errors"].append(f"Failed to delete original folder: {str(e)}")
                    return False
            
            self.report["success"] = True
            self.report["total_size"] = sum(f.stat().st_size for f in new_path.rglob('*') if f.is_file())
            return True
        except Exception as e:
            logging.error(f"Moving folder contents failed: {str(e)}")
            self.report["errors"].append(str(e))
            logging.error(traceback.format_exc())
            return False

    def verify_file_copy(self, source, destination):
        self.logger.debug(f"Verifying file copy from {source} to {destination}.")
        # Performs an MD5 checksum comparison to ensure file integrity
        # after copying from the old location to the new one.
        """
        Verifies file integrity after copy using MD5 checksum.
        
        Args:
            source (Path): Source file path
            destination (Path): Destination file path
            
        Returns:
            bool: True if checksums match, False otherwise
        """
        try:
            import hashlib
            
            def get_file_hash(filepath):
                hash_md5 = hashlib.md5()
                with open(filepath, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                return hash_md5.hexdigest()
            
            return get_file_hash(source) == get_file_hash(destination)
        except Exception as e:
            self.logger.error(f"File verification failed: {str(e)}")
            self.logger.error(traceback.format_exc())
            return False
    
    def relocate_folder(self, folder_name, new_base_path, skip_checksum=False, delete_files=False, use_new_location=False, username=None):
        self.logger.debug(f"Initiating relocation for folder: {folder_name}.")
        # Handles the end-to-end process of validating paths, backing up
        # the registry, moving data, and updating registry entries
        # for the specified folder.
        """
        Main relocation function that orchestrates the entire process for a single folder.
        
        Args:
            folder_name (str): Name of the folder to relocate
            new_base_path (str): Base path where the folder will be relocated
            skip_checksum (bool): Skip checksum validation
            delete_files (bool): Delete files after relocation
            use_new_location (bool): Use new location as default
            username (str): Username for which the folder is being relocated
            
        Returns:
            bool: True if relocation successful, False otherwise
        """
        if folder_name not in self.known_folders:
            logging.error(f"Unknown folder: {folder_name}")
            return False
        
        # Get current folder path
        if username:
            if folder_name == "AppData":
                old_path = Path(f"C:/Users/{username}/AppData")
            elif folder_name == "Temp Folders":
                old_path = Path(f"C:/Users/{username}/AppData/Local/Temp")
            elif folder_name == "OneDrive":
                old_path = Path(f"C:/Users/{username}/OneDrive")
            elif folder_name == "Public Folders":
                old_path = Path(f"C:/Users/Public")
            else:
                old_path = Path(f"C:/Users/{username}/{folder_name}")
        else:
            shell = win32com.client.Dispatch("WScript.Shell")
            old_path = Path(shell.SpecialFolders(self.known_folders[folder_name]['id']))
        
        # Construct new path
        new_path = Path(new_base_path) / username / folder_name
        
        # Validate new path
        valid, message = self.validate_path(new_path)
        if not valid:
            logging.error(message)
            self.report["errors"].append(message)
            return False
        
        # Perform relocation steps
        if not self.backup_registry():
            return False
        
        if not self.move_folder_contents(old_path, new_path, skip_checksum, delete_files):
            return False
        
        if not self.update_registry(folder_name, new_path):
            return False
        
        
        return True
    
    def set_default_location(self, folder_name, new_path):
        logging.debug(f"Setting default location for {folder_name} to {new_path}")
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.get_user_shell_folders_path(),
                0, winreg.KEY_SET_VALUE
            )
            
            winreg.SetValueEx(
                key,
                self.known_folders[folder_name]['id'],
                0,
                winreg.REG_EXPAND_SZ,
                str(new_path)
            )
            
            winreg.CloseKey(key)
            logging.info(f"Default location set for {folder_name}: {new_path}")
        except Exception as e:
            logging.error(f"Failed to set default location for {folder_name}: {str(e)}")
            logging.error(traceback.format_exc())

    def restore_backup(self, backup_file):
        logging.debug(f"Restoring registry from backup file: {backup_file}")
        try:
            if self.dry_run:
                logging.info(f"DRY RUN: Would restore registry from {backup_file}")
                return True
            
            result = os.system(f'reg import "{backup_file}"')
            if result == 0:
                logging.info(f"Successfully restored registry from {backup_file}")
                return True
            else:
                logging.error(f"Failed to restore registry from {backup_file}")
                return False
        except Exception as e:
            logging.error(f"Exception occurred while restoring backup: {str(e)}")
            logging.error(traceback.format_exc())
            return False

class RelocationApp(wx.App):
    def OnInit(self):
        self.logger = logging.getLogger('RelocationApp')
        self.logger.debug("Initializing RelocationApp.")
        self.frame = RelocationFrame(None, title="Windows User Folders Relocation Tool")
        self.frame.Show()
        self.logger.info("RelocationFrame displayed.")
        return True

class FolderSelectionFrame(wx.Frame):
    def __init__(self, parent, *args, **kw):
        super(FolderSelectionFrame, self).__init__(parent, *args, **kw)
        
        self.parent = parent
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.select_all_checkbox = wx.CheckBox(self.panel, label="Select All")
        self.SetSizerAndFit(wx.BoxSizer(wx.VERTICAL))
        self.GetSizer().Add(self.panel, 1, wx.EXPAND | wx.ALL, 5)
        
        self.SetSize((300, 400))
        self.SetTitle("Select Folders to Relocate")
        self.Centre()
    
    def on_select_all(self, event):
        select_all = self.select_all_checkbox.GetValue()
        for checkbox in self.folder_checkboxes.values():
            checkbox.SetValue(select_all)
    
    def on_save(self, event):
        selected_folders = [folder for folder, checkbox in self.folder_checkboxes.items() if checkbox.GetValue()]
        self.parent.set_selected_folders(selected_folders)
        self.Close()

class BackupSelectionFrame(wx.Frame):
    def __init__(self, parent, *args, **kw):
        super(BackupSelectionFrame, self).__init__(parent, *args, **kw)
        
        self.parent = parent
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.backup_list = wx.ListBox(self.panel)
        self.sizer.Add(wx.StaticText(self.panel, label="Select Backup to Restore:"), 0, wx.ALL, 5)
        self.sizer.Add(self.backup_list, 1, wx.ALL | wx.EXPAND, 5)
        
        self.backup_details = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.sizer.Add(wx.StaticText(self.panel, label="Backup Details:"), 0, wx.ALL, 5)
        self.sizer.Add(self.backup_details, 1, wx.ALL | wx.EXPAND, 5)
        
        self.load_backups()
        
        self.backup_list.Bind(wx.EVT_LISTBOX, self.on_select_backup)
        
        self.restore_button = wx.Button(self.panel, label="Restore Selected Backup")
        self.restore_button.Bind(wx.EVT_BUTTON, self.on_restore)
        self.sizer.Add(self.restore_button, 0, wx.ALL | wx.CENTER, 5)
        
        self.panel.SetSizerAndFit(self.sizer)
        self.SetSizerAndFit(wx.BoxSizer(wx.VERTICAL))
        self.GetSizer().Add(self.panel, 1, wx.EXPAND | wx.ALL, 5)
        
        self.SetSize((400, 400))
        self.SetTitle("Restore from Backup")
        self.Centre()
    
    def load_backups(self):
        backup_dir = Path("backups")
        backups = list(backup_dir.glob("*.reg"))
        for backup in backups:
            self.backup_list.Append(f"{backup.name} - {datetime.fromtimestamp(backup.stat().st_mtime)}")
    
    def on_select_backup(self, event):
        selection = self.backup_list.GetSelection()
        if selection == wx.NOT_FOUND:
            self.backup_details.SetValue("")
            return
        
        backup_file = Path("backups") / self.backup_list.GetString(selection).split(" - ")[0]
        details = self.get_backup_details(backup_file)
        self.backup_details.SetValue(details)
    
    def get_backup_details(self, backup_file):
        try:
            with open(backup_file, 'r') as file:
                content = file.read()
            return content
        except Exception as e:
            return f"Failed to read backup details: {str(e)}"
    
    def on_restore(self, event):
        selection = self.backup_list.GetSelection()
        if selection == wx.NOT_FOUND:
            wx.MessageBox("Please select a backup to restore.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        backup_file = Path("backups") / self.backup_list.GetString(selection).split(" - ")[0]
        confirm = wx.MessageBox(f"Are you sure you want to restore from backup '{backup_file}'?", "Confirm", wx.YES_NO | wx.ICON_QUESTION)
        if confirm != wx.YES:
            return
        
        if self.parent.relocator.restore_backup(backup_file):
            wx.MessageBox("Registry restored successfully.", "Success", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Failed to restore registry.", "Error", wx.OK | wx.ICON_ERROR)
        self.Close()

class RelocationFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(RelocationFrame, self).__init__(*args, **kw)
        self.logger = logging.getLogger('RelocationFrame')
        self.logger.debug("Initializing RelocationFrame.")
        
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.user_choice = wx.Choice(self.panel, choices=self.get_users())
        self.sizer.Add(wx.StaticText(self.panel, label="Select User:"), 0, wx.ALL, 5)
        self.sizer.Add(self.user_choice, 0, wx.ALL | wx.EXPAND, 5)
        
        self.drive_choice = wx.Choice(self.panel, choices=self.get_drives())
        self.sizer.Add(wx.StaticText(self.panel, label="Select Drive:"), 0, wx.ALL, 5)
        self.sizer.Add(self.drive_choice, 0, wx.ALL | wx.EXPAND, 5)
        
        self.select_folders_button = wx.Button(self.panel, label="Select Folders")
        self.select_folders_button.Bind(wx.EVT_BUTTON, self.on_select_folders)
        self.sizer.Add(self.select_folders_button, 0, wx.ALL | wx.CENTER, 5)
        
        self.dry_run_checkbox = wx.CheckBox(self.panel, label="Dry Run")
        self.sizer.Add(self.dry_run_checkbox, 0, wx.ALL, 5)
        
        self.no_backup_checkbox = wx.CheckBox(self.panel, label="Skip Registry Backup")
        self.sizer.Add(self.no_backup_checkbox, 0, wx.ALL, 5)
        
        self.skip_checksum_checkbox = wx.CheckBox(self.panel, label="Skip Checksum Validation")
        self.sizer.Add(self.skip_checksum_checkbox, 0, wx.ALL, 5)
        
        self.delete_files_checkbox = wx.CheckBox(self.panel, label="Delete Files After Relocation")
        self.sizer.Add(self.delete_files_checkbox, 0, wx.ALL, 5)
        
        self.use_new_location_checkbox = wx.CheckBox(self.panel, label="Use New Location as Default")
        self.sizer.Add(self.use_new_location_checkbox, 0, wx.ALL, 5)
        
        self.clear_log_checkbox = wx.CheckBox(self.panel, label="Clear Log on Exit")
        self.sizer.Add(self.clear_log_checkbox, 0, wx.ALL, 5)
        
        self.log_file_text = wx.TextCtrl(self.panel, value="")
        self.sizer.Add(wx.StaticText(self.panel, label="Log File (optional):"), 0, wx.ALL, 5)
        self.sizer.Add(self.log_file_text, 0, wx.ALL | wx.EXPAND, 5)
        
        # Add Overwrite Options
        self.overwrite_files_checkbox = wx.CheckBox(self.panel, label="Overwrite Existing Files")
        self.sizer.Add(self.overwrite_files_checkbox, 0, wx.ALL, 5)
        
        self.overwrite_folders_checkbox = wx.CheckBox(self.panel, label="Overwrite Existing Folders")
        self.sizer.Add(self.overwrite_folders_checkbox, 0, wx.ALL, 5)
        
        self.overwrite_all_checkbox = wx.CheckBox(self.panel, label="Overwrite All")
        self.sizer.Add(self.overwrite_all_checkbox, 0, wx.ALL, 5)
        
        self.start_button = wx.Button(self.panel, label="Start Relocation")
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start)
        self.sizer.Add(self.start_button, 0, wx.ALL | wx.CENTER, 5)
        
        self.restore_button = wx.Button(self.panel, label="Restore from Backup")
        self.restore_button.Bind(wx.EVT_BUTTON, self.on_restore)
        self.sizer.Add(self.restore_button, 0, wx.ALL | wx.CENTER, 5)
        
        self.progress_gauge = wx.Gauge(self.panel, range=100, size=(300, 25), style=wx.GA_HORIZONTAL)
        self.sizer.Add(self.progress_gauge, 0, wx.ALL | wx.EXPAND, 5)
        
        self.panel.SetSizerAndFit(self.sizer)
        self.SetSizerAndFit(wx.BoxSizer(wx.VERTICAL))
        self.GetSizer().Add(self.panel, 1, wx.EXPAND | wx.ALL, 5)
        
        self.SetSize((400, 600))
        self.SetTitle("Windows User Folders Relocation Tool")
        self.Centre()
        
        self.selected_folders = []
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
    def get_users(self):
        # Get a list of user profiles on the system
        users = []
        for profile in Path("C:/Users").iterdir():
            if profile.is_dir():
                users.append(profile.name)
        return users
    
    def get_drives(self):
        return [f"{d}:\\" for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f"{d}:\\")]
    
    def on_select_folders(self, event):
        folder_selection_frame = FolderSelectionFrame(self, title="Select Folders to Relocate")
        folder_selection_frame.Show()
    
    def set_selected_folders(self, folders):
        self.selected_folders = folders
    
    def on_start(self, event):
        self.logger.debug("Start Relocation button clicked.")
        username = self.user_choice.GetStringSelection()
        target_drive = self.drive_choice.GetStringSelection()
        self.logger.info(f"Selected user: {username}, Target drive: {target_drive}")
        
        if not username:
            self.logger.error("No user selected.")
            wx.MessageBox("Please select a user.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        if not target_drive:
            self.logger.error("No target drive selected.")
            wx.MessageBox("Please select a target drive.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        confirm = wx.MessageBox(f"Are you sure you want to relocate folders for user '{username}' to drive '{target_drive}'?", "Confirm", wx.YES_NO | wx.ICON_QUESTION)
        self.logger.debug("User confirmation received.")
        if confirm != wx.YES:
            self.logger.info("User canceled the relocation process.")
            return
        
        if not self.selected_folders:
            self.logger.error("No folders selected for relocation.")
            wx.MessageBox("Please select at least one folder to relocate.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        dry_run = self.dry_run_checkbox.GetValue()
        no_backup = self.no_backup_checkbox.GetValue()
        skip_checksum = self.skip_checksum_checkbox.GetValue()
        delete_files = self.delete_files_checkbox.GetValue()
        use_new_location = self.use_new_location_checkbox.GetValue()
        log_file = self.log_file_text.GetValue()
        
        overwrite_files = self.overwrite_files_checkbox.GetValue()
        overwrite_folders = self.overwrite_folders_checkbox.GetValue()
        overwrite_all = self.overwrite_all_checkbox.GetValue()
        
        self.start_button.Disable()
        self.relocator = UserFolderRelocator(
            dry_run=dry_run,
            skip_backup=no_backup,
            log_file=log_file if log_file else None,
            gui=self,
            overwrite_files=overwrite_files,
            overwrite_folders=overwrite_folders,
            overwrite_all=overwrite_all
        )
        try:
            self.logger.debug("Starting folder relocation process.")
            for folder in self.selected_folders:
                self.logger.info(f"Relocating folder: {folder}")
                success = self.relocator.relocate_folder(folder, target_drive)
                if success:
                    self.logger.info(f"Successfully relocated folder: {folder}")
                else:
                    self.logger.error(f"Failed to relocate folder: {folder}")
        except Exception as e:
            self.logger.error(f"Exception during folder relocation: {str(e)}")
            self.logger.error(traceback.format_exc())
            wx.MessageBox("An unexpected error occurred during relocation.", "Error", wx.OK | wx.ICON_ERROR)
        
        self.show_report()
        self.start_button.Enable()
    
    def show_report(self):
        self.logger.debug("Generating relocation report.")
        report = self.relocator.report
        report_message = f"Relocation {'succeeded' if report['success'] else 'failed'}.\n"
        report_message += f"Total files moved: {len(report['moved_files'])}\n"
        report_message += f"Total size moved: {report['total_size']} bytes\n"
        if report['errors']:
            report_message += "Errors:\n" + "\n".join(report['errors'])
            self.logger.error("Errors encountered during relocation:")
            for error in report['errors']:
                self.logger.error(error)
        
        wx.MessageBox(report_message, "Relocation Report", wx.OK | wx.ICON_INFORMATION)
        self.logger.info("Relocation report displayed to the user.")
    
    def on_restore(self, event):
        logging.debug("User clicked 'Restore from Backup'.")
        backup_selection_frame = BackupSelectionFrame(self, title="Restore from Backup")
        backup_selection_frame.Show()
        logging.info("BackupSelectionFrame opened.")
    
    def on_close(self, event):
        if self.clear_log_checkbox.GetValue():
            try:
                os.remove(self.relocator.log_file)
                logging.info("Log file cleared on exit.")
            except Exception as e:
                logging.error(f"Failed to clear log file: {str(e)}")
        self.Destroy()
    
    def update_progress(self, copied_files, total_files):
        self.progress_gauge.SetValue(int((copied_files / total_files) * 100))
        self.progress_gauge.SetLabel(f"Copied {copied_files} of {total_files} files")
    
        sys.exit(1)
    def update_status(self, message):
        self.SetStatusText(message)

def main():
    """
    Launches GUI only.
    """
    # OS check to ensure the script runs only on Windows
    if platform.system() != "Windows":
        logging.error("This script can only be run on Windows operating systems.")
        sys.exit(1)
        
    app = RelocationApp(False)
    app.MainLoop()

if __name__ == "__main__":
    main()

        
    app = RelocationApp(False)
    app.MainLoop()

if __name__ == "__main__":
    main()
