# CodeSnapper

A simple command-line tool to create code snapshots by combining multiple files into a single file with comments.

## Installation

```bash
pip install codesnapper
```

## Usage

1. Run `codesnap` in your project directory
2. Edit the created `snapshot.txt` file to list the files you want to include:
   ```
   main.py "Main application file"
   utils/helper.py "Helper functions"
   ```
3. Run `codesnap` again to generate the snapshot
   - Creates `code-snapshot.txt` with all files combined
   - Automatically copies content to clipboard

## Features

- 📝 Combines multiple files into a single snapshot
- 💭 Supports comments for each file
- 📋 Automatically copies to clipboard
- 🎨 Colorful terminal output
- 🔄 Relative path support

## License

MIT
