# File Classifier

A powerful, cross-platform Python utility for organizing files and folders automatically based on extensions, folder names, or timestamps.

[![EN](https://img.shields.io/badge/lang-English-blue.svg)](./README.md)
[![ID](https://img.shields.io/badge/lang-Indonesia-red.svg)](./translations/README.id.md)
[![FR](https://img.shields.io/badge/lang-France-orange.svg)](./translations/README.fr.md)
[![ES](https://img.shields.io/badge/lang-Spanish-yellow.svg)](./translations/README.es.md)
[![ZH](https://img.shields.io/badge/lang-Mandarin-teal.svg)](./translations/README.zh.md)

## Features

- **Multiple Classification Methods**:
  - **Extension-based**: Classifies files into categories based on their extensions
  - **Time-based**: Organizes files by creation, modification, or access time
  - **Folder classification**: Categorizes folders based on common naming patterns

- **File Categories**:
  - Documents (PDF, DOC, TXT, etc.)
  - Images (JPG, PNG, GIF, etc.)
  - Audio (MP3, WAV, FLAC, etc.)
  - Videos (MP4, AVI, MKV, etc.)
  - Archives (ZIP, RAR, 7Z, etc.)
  - Code (PY, JAVA, HTML, etc.)
  - Executables (EXE, MSI, APP, etc.)
  - Others (for extensions not in the above categories)

- **Folder Categories**:
  - Projects: For development and project-related folders
  - Backups: For backup and archived content
  - Documents: For document and report folders
  - Media: For photos, videos, music folders
  - Downloads: For download folders
  - Applications: For software and apps
  - Data: For datasets and databases
  - Web: For web-related content
  - Dated: For folders with date patterns (auto-detected)
  - Versioned: For folders with version patterns (auto-detected)
  - Uncategorized: For folders that don't match any patterns

- **Operation Modes**:
  - Move (default): Moves files/folders to target directories
  - Copy: Creates copies instead of moving
  - Symlink: Creates symbolic links to original files/folders
  - Dry-run: Shows what would happen without making changes

- **Cross-Platform Compatibility**:
  - Works on Windows, macOS, and Linux

## Requirements

- Python 3.6 or higher
- No additional libraries required (uses standard library only)

## Installation

Download the script and make it executable:

```bash
chmod +x file_classifier.py
```

Or run it directly with Python:

```bash
python file_classifier.py [options]
```

## Usage

### Basic Usage

```bash
python file_classifier.py SOURCE_DIR [TARGET_DIR]
```

If `TARGET_DIR` is not specified, files will be organized in a new directory called `./classified`.

### Common Options

```
-l, --symlinks       Create symlinks instead of moving files
-c, --copy           Copy files instead of moving them
-d, --dry-run        Show what would be done without actually doing it
-f, --folders        Include folders in the classification
```

### Classification Methods

```
-e, --extensions     Classify by file extensions (default behavior)
-t, --time           Organize by time attribute
```

### Time-based Organization Options

```
--time-attr {modified,created,accessed}
                     Time attribute to use (default: modified)
--time-format FORMAT
                     Time format for directories (default: '%Y-%m' for year-month)
```

## Examples

### Extension-based Organization

```bash
# Classify all files in Downloads folder by extension
python file_classifier.py ~/Downloads ~/Organized

# Classify files and folders, create copies instead of moving
python file_classifier.py ~/Documents ~/Organized -f -c

# Create symlinks instead of moving files
python file_classifier.py ~/Pictures ~/Organized -l

# Preview what would happen without making any changes
python file_classifier.py ~/Desktop -d
```

### Time-based Organization

```bash
# Organize files by their modification time (year-month)
python file_classifier.py ~/Documents ~/TimeOrganized -t

# Organize by creation date with year-month-day format
python file_classifier.py ~/Photos ~/Chronological -t --time-attr created --time-format "%Y-%m-%d"

# Organize files and folders by access time
python file_classifier.py ~/Downloads ~/AccessOrganized -t --time-attr accessed -f
```

## FAQ

**Q: What happens if a file or folder already exists in the target directory?**
A: The script will skip it and log a warning message.

**Q: Will the organization preserve the directory structure?**
A: No, all files are flattened to the corresponding category directories. For hierarchical organization, consider using the time-based organization with a hierarchical format like `%Y/%m/%d`.

**Q: Can I customize file categories?**
A: Yes, you can edit the `FILE_CATEGORIES` dictionary in the script to add or modify categories.

## License

This utility is released under the MIT License. Feel free to use, modify, and distribute it.
