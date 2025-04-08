from flask import Flask, render_template, request, jsonify, g
import os
import sys
import psutil
import re
import pyperclip # Keep for potential clipboard functionality later
import tiktoken
import threading
import time
import socket
from datetime import datetime
from functools import wraps

# Assuming core logic might be refactored here or imported
# from codesnap_core import list_files_recursive, generate_snapshot_content

# Flask should now find the 'templates' folder relative to app.py within the package
app = Flask(__name__)

# Placeholder for root directory - will default to where app is run
PROJECT_ROOT = os.getcwd()

# Global variables for activity tracking
last_activity_time = datetime.now()
idle_timeout = 300  # 5 minutes in seconds
shutdown_flag = False
shutdown_timer = None
IGNORE_DIRS = {'.git', '.vscode', '__pycache__', 'node_modules', 'venv'}
IGNORE_FILES = {'.DS_Store'}

def build_file_tree(dir_path):
    """Recursively builds a file tree structure, sorting folders before files."""
    folders = []
    files = []
    try:
        for item in os.listdir(dir_path):
            full_path = os.path.join(dir_path, item)
            rel_path = os.path.relpath(full_path, PROJECT_ROOT)

            if os.path.isdir(full_path):
                if item not in IGNORE_DIRS and not item.startswith('.'):
                    children = build_file_tree(full_path)
                    # Only add directories if they contain something OR if we want to show empty folders
                    if children: # Modify this condition if you want to show empty folders
                        folders.append({'name': item, 'path': rel_path, 'type': 'directory', 'children': children})
            else:
                if item not in IGNORE_FILES and not item.startswith('.'):
                    files.append({'name': item, 'path': rel_path, 'type': 'file'})

        # Sort folders and files alphabetically by name
        folders.sort(key=lambda x: x['name'])
        files.sort(key=lambda x: x['name'])

        # Combine sorted lists (folders first)
        tree = folders + files

    except OSError as e:
        print(f"Error accessing {dir_path}: {e}", file=sys.stderr) # Log error
        return [] # Return empty list on permission errors etc.
    return tree


# --- Activity Tracking and Idle Timeout ---
def update_activity_time():
    """Update the last activity time to now."""
    global last_activity_time
    last_activity_time = datetime.now()

def track_activity(f):
    """Decorator to track activity for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        update_activity_time()
        return f(*args, **kwargs)
    return decorated_function

def check_idle_timeout():
    """Check if the server has been idle for too long and shut it down if needed."""
    global shutdown_flag
    while not shutdown_flag:
        time.sleep(10)  # Check every 10 seconds
        idle_time = (datetime.now() - last_activity_time).total_seconds()
        if idle_time > idle_timeout:
            print(f"Server idle for {idle_time:.1f} seconds, shutting down...")
            shutdown_flag = True
            # Use a separate thread to shut down the server to avoid deadlock
            threading.Thread(target=lambda: os.kill(os.getpid(), 15)).start()
            break

@app.route('/')
@track_activity
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/files')
@track_activity
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
             return f"Error reading binary file: {str(e)}" # Correct indentation
    except FileNotFoundError:
        return f"Error: File not found at {file_path}" # Correct indentation
    except Exception as e:
        return f"Error reading file: {str(e)}" # Correct indentation
# --- End Core File Reading Logic ---

# --- Token Counting Logic ---
def count_tokens(text, model="cl100k_base"):
    """Counts tokens in a string using tiktoken."""
    # Handle potential non-string input gracefully
    if not isinstance(text, str):
        return 0
    # Avoid counting tokens for error messages or binary placeholders
    if text.startswith("Error:") or text.startswith("--- BINARY CONTENT"):
        return 0
    try:
        # Attempt to get encoding for a common default model
        encoding = tiktoken.get_encoding(model)
    except Exception:
        # Fallback if the specific model encoding isn't available
        try:
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo") # A common fallback
        except Exception:
             # Absolute fallback: simple word count (very inaccurate)
             print("Warning: tiktoken encoding not found, falling back to word count.", file=sys.stderr)
             return len(text.split())

    try:
        num_tokens = len(encoding.encode(text))
    except Exception as e:
        print(f"Warning: tiktoken encoding failed for text snippet: {e}", file=sys.stderr)
        num_tokens = 0 # Or fallback to word count?
    return num_tokens
# --- End Token Counting Logic ---


@app.route('/api/generate', methods=['POST'])
@track_activity
def generate_snapshot():
    """API endpoint to generate the code snapshot using selected files."""
    selected_files = request.json.get('files', [])
    if not selected_files:
        return jsonify({"error": "No files selected"}), 400

    combined_content = ""
    total_token_count = 0
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
            # Add individual file token count (optional, could be large)
            file_token_count = count_tokens(content)
            total_token_count += file_token_count # Accumulate total tokens
            # Add token count in header?
            header = f"--- START FILE: {rel_path} ({file_token_count} tokens) ---\n\n"
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
    summary = f"--- SNAPSHOT SUMMARY: Processed {processed_count} files, encountered {error_count} errors. Total Tokens: {total_token_count} ---\n\n"
    combined_content = summary + combined_content

    # Clipboard functionality is less practical/reliable in a web server context
    # pyperclip.copy(combined_content) # Removed for now

    return jsonify({"snapshot": combined_content, "total_token_count": total_token_count})


@app.route('/api/file_content')
@track_activity
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
             # Count tokens for valid content
             token_count = count_tokens(content)
             return jsonify({"error": content, "token_count": 0}), 500 # Return 0 tokens on error
        else:
             # Count tokens for valid content
             token_count = count_tokens(content)
             return jsonify({"content": content, "language": lang, "token_count": token_count})
    else:
        return jsonify({"error": "File not found or is not a file"}), 404


def start_server():
    """Checks for existing instances and starts the Flask server."""
    global shutdown_flag
    
    # Reset shutdown flag
    shutdown_flag = False
    
    # --- Single Instance Check (Run only if not in Flask reloader process) ---
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        current_pid = os.getpid()
        
        print("Checking for existing instances...")
        
        # Try to kill any existing Flask processes that might be running our application
        # We'll use a more targeted approach that doesn't require elevated privileges
        found_instances = False
        
        # Check for Python processes that might be running our application
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Skip our own process
                if proc.info['pid'] == current_pid:
                    continue
                
                # Check if this is likely our application
                is_our_app = False
                if proc.info.get('cmdline'):
                    cmd_str = ' '.join(proc.info['cmdline'])
                    # Look for key identifiers in the command line
                    if 'python' in cmd_str.lower() and ('codesnap' in cmd_str or 'flask' in cmd_str.lower()):
                        is_our_app = True
                
                # Also check the process name
                if 'codesnap' in proc.info.get('name', '').lower():
                    is_our_app = True
                
                if is_our_app:
                    found_instances = True
                    print(f"Found potential CodeSnapper instance (PID: {proc.info['pid']}). Terminating...")
                    try:
                        process = psutil.Process(proc.info['pid'])
                        process.terminate()
                        try:
                            process.wait(timeout=3)
                            print(f"Terminated process {proc.info['pid']}.")
                        except psutil.TimeoutExpired:
                            print(f"Process {proc.info['pid']} did not terminate in time. Killing...")
                            process.kill()
                            print(f"Killed process {proc.info['pid']}.")
                    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                        print(f"Could not terminate process {proc.info['pid']}: {e}")
                    except Exception as e:
                        print(f"Error handling process {proc.info['pid']}: {e}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # If we found and terminated instances, give them a moment to fully release resources
        if found_instances:
            print("Waiting for terminated processes to release resources...")
            time.sleep(1)  # Short delay to ensure port is released
                
        print("Instance check complete.")
    # --- End Single Instance Check ---

    # Start the idle timeout checker thread
    timeout_thread = threading.Thread(target=check_idle_timeout, daemon=True)
    timeout_thread.start()
    print(f"Idle timeout checker started (server will shut down after {idle_timeout} seconds of inactivity)")
    
    # Try to start the server on the default port, and if it fails, try the next port
    default_port = 4789
    max_port = 4799  # Try up to 10 ports
    
    for port in range(default_port, max_port + 1):
        try:
            # Check if the port is available
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                # If we get here, the port is available
                s.close()
                
            print(f"Starting Flask server on port {port}...")
            # Note: Debug mode is convenient but insecure for production
            app.run(debug=True, port=port, use_reloader=False)
            break  # If server starts successfully, break the loop
        except OSError as e:
            if port < max_port:
                print(f"Port {port} is in use, trying port {port + 1}...")
            else:
                print(f"All ports from {default_port} to {max_port} are in use. Please free up a port and try again.")
                sys.exit(1)

if __name__ == '__main__':
    start_server() # Call the function for direct execution