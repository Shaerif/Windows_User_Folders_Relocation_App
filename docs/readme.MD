# 🗂️ Windows User Folders Relocation Tool

A robust Python utility for safely relocating Windows user folders to different locations while maintaining system integrity.

## ✨ Features

- 🛡️ **Safety First**
  - 🗄️ Registry automatic backup
  - 🔍 File integrity verification
  - 📊 Progress tracking
  - 📝 Detailed logging
  - 💾 Space verification
  - 🔒 Admin privileges check

- 📁 **Supported Folders**
  - 📄 Documents
  - 📥 Downloads
  - 🖼️ Pictures
  - 🎵 Music
  - 🎥 Videos
  - 🖥️ Desktop

- **Overwrite Options**
  - 🔄 Overwrite Existing Files
  - 📂 Overwrite Existing Folders
  - 🔄🔂 Overwrite All Existing Files and Folders

## 🛠️ Requirements

- 🖥️ Windows 10/11
- 🐍 Python 3.8+
- 🔑 Administrator privileges
- 📦 Required Python packages (see requirements.txt)
- 🖥️ wxPython for GUI support

## 📥 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/windows-user-folders-relocation-tool.git
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 🛡️ Operating System Compatibility

- 🖥️ **Supported OS:** Windows 10/11
- ❗ **Unsupported OS:** Other operating systems are not supported.

## 📦 Required Python Packages

Ensure all dependencies are installed by running:
```bash
pip install -r requirements.txt
```

## 🌐 Dynamic Path Handling

The tool automatically detects user directories and available drives, making it compatible with any Windows setup.

## 🛠️ Compiling to Executable

To compile the script to an executable format for Windows, you can use `PyInstaller`.

1. **Install PyInstaller:**
```bash
pip install pyinstaller
```

2. **Compile the script:**
```bash
pyinstaller --onefile folder-relocator.py
```

This will create a single executable file in the `dist` directory.

## 🚀 Usage

1. **Command Line Usage:**
```bash
python folder-relocator.py --target <TARGET_PATH> --overwrite-all
```
- Replace `<TARGET_PATH>` with your desired target path.
- Use other arguments as needed based on `--help`.

2. **CLI Overwrite Options:**
- `--overwrite-files`: Overwrite existing files in the target location.
- `--overwrite-folders`: Overwrite existing folders in the target location.
- `--overwrite-all`: Overwrite all existing files and folders in the target location.

3. **GUI Usage:**
- If no `--target` argument is provided, the GUI will launch by default, allowing you to select the target drive and folders to relocate.
- **Overwrite Options in GUI:**
  - **Overwrite Existing Files:** Check to allow overwriting of existing files.
  - **Overwrite Existing Folders:** Check to allow overwriting of existing folders.
  - **Overwrite All:** Check to allow overwriting of all existing files and folders without individual prompts.

## 🛡️ Safety Measures

1. **Pre-move Checks:**
   - 🔑 Administrative privileges verification
   - 💾 Disk space validation (minimum 5GB required)
   - 📂 Path accessibility check
   - 🗄️ Registry backup creation

2. **During Move:**
   - 📊 Progress tracking
   - 🔍 File integrity verification
   - 🗂️ Original location preservation
   - 🔗 Junction point creation

3. **Post-move Verification:**
   - 📄 File count matching
   - 🔍 Checksum verification
   - 📝 Registry update confirmation

## 📁 Folders That Can Be Relocated

### Documents
- **Default:** `C:\Users\[YourUsername]\Documents`
- **Purpose:** For personal documents (e.g., Word, Excel, PDFs).
- **Relocation:** Can be relocated via the folder's Properties > Location tab.

### Downloads
- **Default:** `C:\Users\[YourUsername]\Downloads`
- **Purpose:** Default location for internet downloads.
- **Relocation:** Can be relocated through Properties > Location.

### Pictures
- **Default:** `C:\Users\[YourUsername]\Pictures`
- **Purpose:** Stores images, photos, and screenshots.
- **Relocation:** Can be moved using the Location tab.

### Music
- **Default:** `C:\Users\[YourUsername]\Music`
- **Purpose:** For music and audio files.
- **Relocation:** Relocatable via Properties > Location.

### Videos
- **Default:** `C:\Users\[YourUsername]\Videos`
- **Purpose:** For video files and recordings.
- **Relocation:** Can be moved through the Location tab.

### Desktop
- **Default:** `C:\Users\[YourUsername]\Desktop`
- **Purpose:** Stores files and shortcuts visible on the desktop.
- **Relocation:** Can be relocated.

### AppData (Partially)
- **Default:** `C:\Users\[YourUsername]\AppData`
- **Purpose:** Stores application-specific data.
- **Subfolders:** Local, Roaming, LocalLow
- **Caution:** Moving AppData requires symbolic links to avoid breaking paths for applications.

### Temp Folders
- **Default:**
  - System Temp: `C:\Windows\Temp`
  - User Temp: `C:\Users\[YourUsername]\AppData\Local\Temp`
- **Purpose:** Stores temporary files used by the system and applications.
- **Relocation:** Can be redirected via Environment Variables settings.

### OneDrive
- **Default:** `C:\Users\[YourUsername]\OneDrive`
- **Purpose:** Sync location for OneDrive files.
- **Relocation:** Can be moved through OneDrive settings.

### Public Folders
- **Default:** `C:\Users\Public`
- **Purpose:** For shared files among all users.
- **Relocation:** Can be moved manually or via symbolic links.

### Default Save Locations for Libraries
- **Includes:** Documents, Pictures, Music, Videos libraries.
- **Relocation:** Can be redirected via Settings > System > Storage > Change where new content is saved.

## 🗂️ File Structure of Moved Files

When relocating user folders, the files will be organized under a folder named after the username on the target drive. For example, if the target drive is `D:` and the username is `[YourUsername]`, the files will be moved to:

```
D:\
  └── [YourUsername]\
      ├── Documents\
      ├── Downloads\
      ├── Pictures\
      ├── Music\
      ├── Videos\
      └── Desktop\
```

## 🛡️ Running as Administrator

To avoid issues while moving files, it is recommended to run the script as an administrator. You can do this by right-clicking on the script or executable and selecting "Run as administrator".

## 🛡️ Running the CLI as Administrator

To ensure the CLI operates with the necessary permissions, follow these steps:

1. **Open Command Prompt as Administrator:**
   - Press `Win + X` and select **Command Prompt (Admin)** or **Windows PowerShell (Admin)**.
   - Alternatively, search for `cmd` in the Start menu, right-click **Command Prompt**, and choose **Run as administrator**.

2. **Navigate to the Project Directory:**
```bash
cd path/to/Windows_User_Folders_Relocation_App
```

3. **Execute the CLI Script:**
```bash
python folder-relocator-cli.py --target <TARGET_PATH> --overwrite-all
```
- Replace `<TARGET_PATH>` with your desired target path.
- Use other arguments as needed based on `--help`.

## 🐞 Troubleshooting Errors

If you encounter errors similar to those in your logs, consider the following steps:

1. **Permission Denied ([WinError 5]):**
   - **Ensure Admin Privileges:** Double-check that the CLI is running with administrative rights.
   - **Close Open Applications:** Make sure no applications are using the folders you intend to relocate.
   - **Antivirus Interference:** Temporarily disable antivirus software that might restrict folder modifications.

2. **File Not Found ([WinError 2] & [WinError 3]):**
   - **Verify Paths:** Ensure that the source and target paths exist and are correctly specified.
   - **Check Folder Names:** Confirm that folder names match exactly, including case sensitivity.

3. **Logging and Error Details:**
   - **Review Log Files:** Check the log files located in `WindowsUserFoldersRelocation/logs/` for detailed error messages.
   - **Example Log Analysis:**
     ```
     2025-01-03 07:29:34,195 - ERROR - Moving folder contents failed: [Errno 13] Permission denied: 'C:\\Users\\[YourUsername]\\Documents'
     ```
     - **Interpretation:** The script lacked sufficient permissions to move the `Documents` folder.
     - **Action:** Ensure the CLI is run as an administrator and that no processes are locking the folder.

## 🔄 Ensuring CLI and GUI Consistency

Both the CLI and GUI should exhibit similar behaviors and handle errors uniformly. To achieve this:

1. **Consistent Logging:**
   - Ensure both interfaces log errors and actions to the same log files.
   - Review log messages to confirm they follow a consistent format.

2. **Error Handling:**
   - Implement uniform error checks in both CLI and GUI scripts.
   - Provide clear and actionable error messages to the user.

3. **Permissions Verification:**
   - Both interfaces should verify and request administrative privileges before performing operations.
   - Consistent prompts and escalation methods enhance reliability.

4. **Testing:**
   - Test both CLI and GUI with identical parameters to ensure they produce the same outcomes.
   - Validate that errors encountered in CLI are reproducible in the GUI and vice versa.

By following these guidelines and implementing the necessary code modifications, you can ensure that both the CLI and GUI operate seamlessly and handle permissions and errors effectively.

## ❓ Common Issues and Solutions

1. **Access Denied:**
   - Run as administrator
   - Close all applications using target folders

2. **Insufficient Space:**
   - Free up space on target drive
   - Choose a different location

3. **File in Use:**
   - Close all applications
   - Restart Windows Explorer

## 💡 Best Practices

1. **Before Moving:**
   - Backup important data
   - Close all applications
   - Run disk check (chkdsk)

2. **Location Selection:**
   - Choose a dedicated partition
   - Ensure adequate free space
   - Use local drives for better performance

## 🛠️ Technical Support

For issues and support:
1. Check the logs in the application directory
2. Open an issue on GitHub
3. Include log files when reporting problems

## 📜 License

Non-Commercial Educational and Non-Profit License - See LICENSE file for details