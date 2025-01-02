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

## 🛠️ Requirements

- 🖥️ Windows 10/11
- 🐍 Python 3.8+
- 🔑 Administrator privileges
- 📦 Required Python packages (see requirements.txt)

## 📥 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/windows-folder-relocator.git
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. **Command Line Usage:**
```bash
python folder-relocator.py --target D:\NewLocation
```

2. **Command Line Options:**
- `--target`: Specify target base directory
- `--folders`: Comma-separated list of folders to move (default: all)
- `--dry-run`: Test run without making changes
- `--no-backup`: Skip registry backup (not recommended)

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