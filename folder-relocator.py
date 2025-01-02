"""
Windows User Folders Relocation Tool
Generic implementation for Windows systems
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

    def __init__(self, dry_run=False, skip_backup=False, log_file=None):
        self.dry_run = dry_run
        self.skip_backup = skip_backup
        self.log_file = log_file or f"folder_relocation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        # Updated known folders with more generic identifiers
        self.known_folders = {
            'Documents': {'id': 'Personal', 'guid': '{F42EE2D3-909F-4907-8871-4C22FC0BF756}'},
            'Downloads': {'id': '{374DE290-123F-4565-9164-39C4925E467B}', 'guid': '{374DE290-123F-4565-9164-39C4925E467B}'},
            'Pictures': {'id': 'My Pictures', 'guid': '{33E28130-4E1E-4676-835A-98395C3BC3BB}'},
            'Music': {'id': 'My Music', 'guid': '{4BD8D571-6D19-48D3-BE97-422220080E43}'},
            'Videos': {'id': 'My Video', 'guid': '{18989B1D-99B5-455B-841C-AB7C74E4DDFC}'},
            'Desktop': {'id': 'Desktop', 'guid': '{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}'}
        }
        
        self.setup_logging()
        
    def setup_logging(self):
        # Configures logging to both a file and console, ensuring
        # progress messages and error details are captured.
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
    
    def is_admin(self):
        # Determines if the script is running with administrative rights.
        # Some operations require elevated privileges to modify registry keys.
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
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
            
        Checks:
        - Path validity
        - Drive existence
        - Sufficient disk space (5GB minimum)
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
            backup_file = f"registry_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.reg"
            os.system(f'reg export "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders" "{backup_file}"')
            logging.info(f"Registry backup created: {backup_file}")
            return True
        except Exception as e:
            logging.error(f"Registry backup failed: {str(e)}")
            return False
    
    def update_registry(self, folder_name, new_path):
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
            logging.info(f"Registry updated for {folder_name}: {new_path}")
            return True
        except Exception as e:
            logging.error(f"Registry update failed for {folder_name}: {str(e)}")
            return False
    
    def move_folder_contents(self, old_path, new_path):
        # Copies the existing user data to the target folder location.
        # Displays progress, verifies file integrity, and creates a
        # junction point to maintain compatibility with system references.
        """
        Safely moves folder contents to the new location with progress tracking
        and verification. Creates a junction point at the old location.
        
        Args:
            old_path (Path): Original folder path
            new_path (Path): Destination folder path
            
        Returns:
            bool: True if move successful, False otherwise
            
        Features:
        - Progress tracking
        - File verification
        - Junction point creation
        - Backup of original folder
        """
        if self.dry_run:
            logging.info(f"DRY RUN: Would move {old_path} to {new_path}")
            return True

        try:
            old_path = Path(old_path)
            new_path = Path(new_path)
            
            # Create destination if it doesn't exist
            new_path.mkdir(parents=True, exist_ok=True)
            
            # Copy files with progress tracking
            total_files = sum(1 for _ in old_path.rglob('*'))
            copied_files = 0
            
            for item in old_path.rglob('*'):
                if item.is_file():
                    relative_path = item.relative_to(old_path)
                    destination = new_path / relative_path
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file with verification
                    shutil.copy2(item, destination)
                    if not self.verify_file_copy(item, destination):
                        raise Exception(f"File verification failed: {item}")
                    
                    copied_files += 1
                    logging.info(f"Progress: {copied_files}/{total_files} files copied")
            
            # Verify total file count
            if sum(1 for _ in new_path.rglob('*')) != total_files:
                raise Exception("File count mismatch after copy")
            
            # Create junction point for compatibility
            if old_path.exists():
                old_path_backup = old_path.with_name(f"{old_path.name}_backup")
                old_path.rename(old_path_backup)
                os.system(f'mklink /J "{old_path}" "{new_path}"')
            
            logging.info(f"Folder contents moved successfully: {old_path} -> {new_path}")
            return True
        except Exception as e:
            logging.error(f"Moving folder contents failed: {str(e)}")
            return False
    
    def verify_file_copy(self, source, destination):
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
            logging.error(f"File verification failed: {str(e)}")
            return False
    
    def relocate_folder(self, folder_name, new_base_path):
        # Handles the end-to-end process of validating paths, backing up
        # the registry, moving data, and updating registry entries
        # for the specified folder.
        """
        Main relocation function that orchestrates the entire process for a single folder.
        
        Args:
            folder_name (str): Name of the folder to relocate
            new_base_path (str): Base path where the folder will be relocated
            
        Returns:
            bool: True if relocation successful, False otherwise
            
        Process:
        1. Validates folder name and new path
        2. Creates registry backup
        3. Moves folder contents
        4. Updates registry
        """
        if folder_name not in self.known_folders:
            logging.error(f"Unknown folder: {folder_name}")
            return False
        
        # Get current folder path
        shell = win32com.client.Dispatch("WScript.Shell")
        old_path = shell.SpecialFolders(self.known_folders[folder_name]['id'])
        
        # Construct new path
        new_path = os.path.join(new_base_path, folder_name)
        
        # Validate new path
        valid, message = self.validate_path(new_path)
        if not valid:
            logging.error(message)
            return False
        
        # Perform relocation steps
        if not self.backup_registry():
            return False
        
        if not self.move_folder_contents(old_path, new_path):
            return False
        
        if not self.update_registry(folder_name, new_path):
            return False
        
        return True

def main():
    # Entry point for the script:
    # 1. Parse arguments
    # 2. Check admin privileges
    # 3. Determine target drive/folder
    # 4. Relocate folders accordingly
    """
    Main entry point of the script.
    Checks for admin privileges and initiates folder relocation process.
    Re-launches with elevated privileges if necessary.
    """
    args = parse_arguments()

    if not UserFolderRelocator().is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return
    
    if not args.target:
        target_drive = choose_drive()
        args.target = target_drive

    relocator = UserFolderRelocator(dry_run=args.dry_run, skip_backup=args.no_backup, log_file=args.log_file)
    
    # Process folder list
    folders_to_move = (args.folders.split(',') if args.folders 
                      else relocator.known_folders.keys())

    # Validate target path
    target_path = Path(args.target).resolve()
    valid, message = relocator.validate_path(target_path)
    if not valid:
        logging.error(f"Invalid target path: {message}")
        return

    # Process each folder
    for folder in folders_to_move:
        if folder not in relocator.known_folders:
            logging.warning(f"Unknown folder: {folder}, skipping")
            continue

        if relocator.relocate_folder(folder, target_path):
            logging.info(f"Successfully relocated {folder}")
        else:
            logging.error(f"Failed to relocate {folder}")

if __name__ == "__main__":
    main()
