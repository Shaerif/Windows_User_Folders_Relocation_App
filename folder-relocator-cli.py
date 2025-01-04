import logging
import traceback
import ctypes
import sys
import os
import platform
import uuid  # Add import for UUID
import getpass  # Add import for getting user ID
from folder_relocator import UserFolderRelocator, parse_arguments  # Assuming module name is folder_relocator.py

def setup_cli_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Set to DEBUG for detailed logs
        format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - [Run ID: %(run_id)s] - [User ID: %(user_id)s] - %(message)s',  # Update format to include user_id
        handlers=[
            logging.FileHandler("cli_relocator.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    user_id = getpass.getuser()  # Get current user ID
    run_id = str(uuid.uuid4())  # Generate a unique run ID
    logger = logging.LoggerAdapter(logger, {'run_id': run_id, 'user_id': user_id})  # Attach run_id and user_id to logger
    logger.info("CLI logging setup complete.")
    logger.debug("CLI logger initialized with DEBUG level.")
    return logger

def run_cli():
    logger = logging.getLogger(__name__)
    user_id = getpass.getuser()  # Get current user ID
    run_id = str(uuid.uuid4())  # Generate a unique run ID
    logger = logging.LoggerAdapter(logger, {'run_id': run_id, 'user_id': user_id})  # Attach run_id and user_id to logger
    logger.debug("Starting CLI run.")
    
    # OS check to ensure the script runs only on Windows
    logger.debug("Checking operating system.")
    if platform.system() != "Windows":
        logger.error("Unsupported operating system. Exiting CLI.")
        print("Error: This script can only be run on Windows operating systems.")
        sys.exit(1)
    
    logger.debug("Parsing command-line arguments.")
    args = parse_arguments()
    logger.info(f"Arguments received: {args}")
    
    logger.debug("Initializing UserFolderRelocator instance.")
    relocator = UserFolderRelocator(
        dry_run=args.dry_run,
        skip_backup=args.no_backup,
        log_file=args.log_file,
        overwrite_files=args.overwrite_files,
        overwrite_folders=args.overwrite_folders,
        overwrite_all=args.overwrite_all
    )
    logger.debug("UserFolderRelocator instance created.")
    
    logger.debug("Checking administrative privileges.")
    if not relocator.is_admin():
        logger.warning("Script not running as administrator. Attempting to elevate privileges.")
        # Re-run the script with admin privileges
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            logger.info("Elevation request sent to the system.")
        except Exception as e:
            logger.error("Failed to elevate privileges.")
            logger.error(traceback.format_exc())
        return
    
    logger.debug("Validating target path.")
    if not args.target:
        logger.error("--target argument is missing.")
        print("Error: --target argument is required in CLI mode.")
        sys.exit(1)
    
    target_path = Path(args.target).resolve()
    logger.debug(f"Resolved target path: {target_path}")
    valid, message = relocator.validate_path(target_path)
    if not valid:
        logger.error(f"Invalid target path: {message}")
        print(f"Invalid target path: {message}")
        sys.exit(1)
    logger.info(f"Target path validated: {target_path}")
    
    logger.debug("Determining folders to move.")
    folders_to_move = args.folders.split(',') if args.folders else relocator.known_folders.keys()
    logger.debug(f"Folders to move: {folders_to_move}")
    
    for folder in folders_to_move:
        logger.debug(f"Processing folder: {folder}")
        if folder not in relocator.known_folders:
            logger.warning(f"Unknown folder: {folder}, skipping.")
            print(f"Unknown folder: {folder}, skipping")
            continue
        
        # Construct new path dynamically
        username = Path.home().name
        new_path = target_path / username / folder
        logger.debug(f"Relocating folder: {folder} to {new_path}")
        
        try:
            success = relocator.relocate_folder(folder, new_path)
            if success:
                logger.info(f"Successfully relocated {folder}.")
                print(f"Successfully relocated {folder}.")
            else:
                logger.error(f"Failed to relocate {folder}.")
                print(f"Failed to relocate {folder}.")
        except Exception as e:
            logger.error(f"Exception occurred while relocating {folder}: {str(e)}")
            logger.error(traceback.format_exc())
            print(f"Failed to relocate {folder} due to an unexpected error.")
    
    logger.debug("Generating relocation report.")
    report = relocator.report
    report_message = f"Relocation {'succeeded' if report['success'] else 'failed'}.\n"
    report_message += f"Total files moved: {len(report['moved_files'])}\n"
    report_message += f"Total size moved: {report['total_size']} bytes\n"
    if report['errors']:
        report_message += "Errors:\n" + "\n".join(report['errors'])
        logger.error("Errors encountered during relocation:")
        for error in report['errors']:
            logger.error(error)
    
    logger.info("Relocation process completed.")
    print(report_message)

if __name__ == "__main__":
    logger = setup_cli_logging()
    run_cli()