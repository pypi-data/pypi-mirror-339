from flask import Flask, render_template, request, jsonify
import os
import sys
import psutil
import re
import pyperclip # Keep for potential clipboard functionality later

# Assuming core logic might be refactored here or imported
# from codesnap_core import list_files_recursive, generate_snapshot_content

# Calculate absolute path to the directory containing app.py
_basedir = os.path.abspath(os.path.dirname(__file__))
# Calculate absolute path to the templates directory
_template_dir = os.path.join(_basedir, 'templates')

# Explicitly set template folder using the calculated absolute path
app = Flask(__name__, template_folder=_template_dir)

# Placeholder for root directory - will default to where app is run
PROJECT_ROOT = os.getcwd()
IGNORE_DIRS = {'.git', '.vscode', '__pycache__', 'node_modules', 'venv'}
IGNORE_FILES = {'.DS_Store'}

def build_file_tree(dir_path):
    """Recursively builds a file tree structure."""
    tree = []
    try:
        for item in sorted(os.listdir(dir_path)):
            full_path = os.path.join(dir_path, item)
            rel_path = os.path.relpath(full_path, PROJECT_ROOT)

            if os.path.isdir(full_path):
                if item not in IGNORE_DIRS and not item.startswith('.'):
                    children = build_file_tree(full_path)
                    if children: # Only add directories if they contain something
                         tree.append({'name': item, 'path': rel_path, 'type': 'directory', 'children': children})
            else:
                if item not in IGNORE_FILES and not item.startswith('.'):
                    tree.append({'name': item, 'path': rel_path, 'type': 'file'})
    except OSError as e:
        print(f"Error accessing {dir_path}: {e}", file=sys.stderr) # Log error
        return [] # Return empty list on permission errors etc.
    return tree


@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/files')
def get_files():
    """API endpoint to list files and directories recursively in a structured tree."""
    file_tree = build_file_tree(PROJECT_ROOT)
    return jsonify(file_tree)

# --- Core File Reading Logic (from codesnap.py) ---
def read_file_content(file_path):
    """
    Reads file content safely as text (UTF-8), and if that fails,
    as binary (converted to hex). Returns content or error message.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            return infile.read()
    except UnicodeDecodeError:
        # If UTF-8 decoding fails, try reading as binary
        try:
            with open(file_path, 'rb') as infile:
                # Indicate that this is hex representation
                return f"--- BINARY CONTENT (HEX) ---\n{infile.read().hex()}"
        except Exception as e:
             return f"Error reading binary file: {str(e)}"
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"
# --- End Core File Reading Logic ---


@app.route('/api/generate', methods=['POST'])
def generate_snapshot():
    """API endpoint to generate the code snapshot using selected files."""
    selected_files = request.json.get('files', [])
    if not selected_files:
        return jsonify({"error": "No files selected"}), 400

    combined_content = ""
    processed_count = 0
    error_count = 0

    # Sort files for consistent output order
    selected_files.sort()

    for rel_path in selected_files:
        # Construct full path safely
        full_path = os.path.abspath(os.path.join(PROJECT_ROOT, rel_path))

        # Security check: Ensure the path is still within the project root
        if not full_path.startswith(os.path.abspath(PROJECT_ROOT)):
             combined_content += f"--- SKIPPED (Outside Root): {rel_path} ---\n\n"
             error_count += 1
             continue

        if os.path.exists(full_path) and os.path.isfile(full_path):
            header = f"--- START FILE: {rel_path} ---\n\n"
            footer = f"\n--- END FILE: {rel_path} ---\n\n"

            content = read_file_content(full_path)
            combined_content += header + content + footer
            processed_count += 1
            if content.startswith("Error"):
                 error_count += 1
        else:
            # This case might be less common now due to how files are selected, but good to keep
            combined_content += f"--- SKIPPED (Not Found/Is Directory): {rel_path} ---\n\n"
            error_count += 1

    # Add a summary line?
    summary = f"--- SNAPSHOT SUMMARY: Processed {processed_count} files, encountered {error_count} errors. ---\n\n"
    combined_content = summary + combined_content

    # Clipboard functionality is less practical/reliable in a web server context
    # pyperclip.copy(combined_content) # Removed for now

    return jsonify({"snapshot": combined_content})


@app.route('/api/file_content')
def get_file_content():
    """API endpoint to get the content of a single file."""
    rel_path = request.args.get('path')
    if not rel_path:
        return jsonify({"error": "No file path provided"}), 400

    # Construct full path safely
    full_path = os.path.abspath(os.path.join(PROJECT_ROOT, rel_path))

    # Security check: Ensure the path is still within the project root
    if not full_path.startswith(os.path.abspath(PROJECT_ROOT)):
         return jsonify({"error": "Access denied: File outside project root"}), 403

    if os.path.exists(full_path) and os.path.isfile(full_path):
        content = read_file_content(full_path)
        # Determine language for highlighting (basic guess based on extension)
        lang = os.path.splitext(rel_path)[1].lstrip('.')
        if content.startswith("Error"):
             return jsonify({"error": content}), 500
        else:
            return jsonify({"content": content, "language": lang})
    else:
        return jsonify({"error": "File not found or is not a file"}), 404


def start_server():
    """Checks for existing instances and starts the Flask server."""
    # --- Single Instance Check (Run only if not in Flask reloader process) ---
    # This check might be less critical when run via entry point, but keep for direct execution
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        current_pid = os.getpid()
        script_name = os.path.basename(__file__) # This will be 'app.py'
        # Consider checking for the 'codesnap' command process name if run via entry point
        print(f"Checking for existing instances...")
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Check if process name or command line matches our script or entry point
                cmd_match = False
                if proc.info.get('cmdline'):
                    cmd_str = ' '.join(proc.info['cmdline'])
                    # Check for both direct execution and entry point execution
                    if script_name in cmd_str or 'codesnap' in cmd_str:
                         cmd_match = True

                if proc.info['pid'] != current_pid and (script_name in proc.info.get('name', '') or cmd_match):
                    print(f"Another instance found running (PID: {proc.info['pid']}). Attempting to terminate...")
                    try:
                        other_process = psutil.Process(proc.info['pid'])
                        other_process.terminate()
                        other_process.wait(timeout=3)
                        print(f"Terminated process {proc.info['pid']}.")
                    except psutil.NoSuchProcess:
                        print(f"Process {proc.info['pid']} already terminated.")
                    except psutil.AccessDenied:
                        print(f"Permission denied to terminate process {proc.info['pid']}. Please terminate it manually.")
                    except psutil.TimeoutExpired:
                        print(f"Process {proc.info['pid']} did not terminate in time. Trying to kill...")
                        try:
                            other_process.kill()
                            print(f"Killed process {proc.info['pid']}.")
                        except Exception as kill_err:
                            print(f"Failed to kill process {proc.info['pid']}: {kill_err}")
                    except Exception as e:
                         print(f"An error occurred while trying to terminate process {proc.info['pid']}: {e}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        print("Instance check complete.")
    # --- End Single Instance Check ---

    print("Starting Flask server...")
    # Note: Debug mode is convenient but insecure for production
    # Consider making debug=False when run via entry point?
    # Disable reloader when run via entry point for stability with instance check
    app.run(debug=True, port=4789, use_reloader=False)

if __name__ == '__main__':
    start_server() # Call the function for direct execution