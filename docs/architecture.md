# Project Architecture

## Overview

The Windows User Folders Relocation Tool is designed to safely relocate user folders to different locations while maintaining system integrity. The project consists of several key components, each contributing to the overall functionality of the tool.

## File Descriptions

### `folder-relocator.py`
This is the main script that handles the relocation logic and the graphical user interface (GUI). It includes the following key components:
- **UserFolderRelocator Class:** Handles the relocation of user folders, including path validation, registry updates, and file movement.
- **RelocationApp Class:** Initializes the wxPython application.
- **RelocationFrame Class:** Defines the main GUI window for the tool.
- **FolderSelectionFrame Class:** Defines a separate window for selecting folders to relocate.
- **BackupSelectionFrame Class:** Defines a separate window for selecting and restoring backups, providing detailed information about each backup.

### `requirements.txt`
This file lists the Python packages required for the project. It includes dependencies for Windows operations, system utilities, logging, progress tracking, and GUI support.

### `docs/readme.md`
The readme file provides an overview of the project, including features, requirements, installation instructions, usage, safety measures, and common issues and solutions.

### `docs/tasks.md`
This file outlines the project's tasks, including ongoing, future, and completed tasks.

### `docs/roadmap.md`
The roadmap file details the project's milestones and provides a detailed list of tasks for each phase of the project.

### `docs/License.md`
This file contains the license information for the project, specifying the permitted and prohibited uses, modification, redistribution, liability, and warranty.

### `docs/CHANGELOG.md`
The changelog file documents all changes made to the project, including new features, changes, and fixes.

### `.gitignore`
This file specifies the files and directories that should be ignored by Git. It includes entries for byte-compiled files, distribution packaging, logs, test reports, and other environment-specific files.

## Files to be Removed

After analyzing the project, the following files are identified as not being linked or used in the project and should be removed:
- **None identified at this time.**

## Conclusion

The Windows User Folders Relocation Tool is a robust and comprehensive solution for relocating user folders on Windows systems. The project's architecture is well-organized, with clear separation of concerns and detailed documentation to support ongoing development and maintenance.
