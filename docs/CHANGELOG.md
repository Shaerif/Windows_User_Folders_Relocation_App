# Changelog

## [Unreleased]

### Added
- Added options in the GUI to skip checksum validation, delete files after relocation, and use the new location as the default for Windows.
- Added detailed information in the readme about relocating user-specific folders and using new locations as default.
- Added instructions for compiling the script to an executable format using `PyInstaller`.
- Added a new `BackupSelectionFrame` class to provide a detailed view of backups and allow users to restore from backups through the GUI.
- Added options in the user interface to overwrite existing files, overwrite existing folders, and overwrite all during the relocation process.
- Updated CLI to include `--overwrite-files`, `--overwrite-folders`, and `--overwrite-all` arguments for handling overwrite behaviors.
- Enhanced `UserFolderRelocator` class to process overwrite options accordingly.

### Changed
- Updated the script to ensure that user files are moved and checksummed before being removed from the original location.
- Updated the `tasks.md` file to outline the project's tasks.
- Updated the `roadmap.md` file to detail the project's milestones.
- Updated the `architecture.md` file to include the new `BackupSelectionFrame` class and its purpose.
- Updated the `relocate_folder` and `move_folder_contents` methods to incorporate overwrite logic based on user selections.
- Modified the GUI layout to include new overwrite options checkboxes.

### Fixed
- Improved error handling for file permission errors during relocation.
- Improved error handling related to folder overwriting scenarios.

## [1.0.1] - 2025-01-03
### Added
- Enabled CLI & GUI dual-run functionality.
- Updated documentation (tasks, roadmap, and architecture) for new dual-run feature.

### Changed
- Minor refinements to existing documentation to reflect the new feature.

## [1.0.0] - 2025-01-02
### Added
- Initial implementation of the Windows User Folders Relocation Tool.
- Core functionality for relocating user folders.
- Logging and progress tracking.
- Safety measures like registry backup and file verification.
