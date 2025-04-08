import os
import sys
import argparse
import re
from colorama import init, Fore, Style
import pyperclip

# Initialize colorama
init()

# Output file name
output_file = "code-snapshot.txt"

def print_success(msg):
    print(f"{Fore.GREEN}✓ {msg}{Style.RESET_ALL}")

def print_info(msg):
    print(f"{Fore.CYAN}ℹ {msg}{Style.RESET_ALL}")

def print_error(msg):
    print(f"{Fore.RED}✗ {msg}{Style.RESET_ALL}")


def parse_snapshot_file(snapshot_path):
    """
    Reads each line of the snapshot file. 
    Each line is expected to have:
       file_path "some optional comment in quotes"
    The comment is optional.
    
    Returns a list of (file_path, comment).
    """
    entries = []
    with open(snapshot_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                # Skip empty lines or commented lines
                continue
            
            # Regex to parse:  file_path  "optional comment"
            #   group(1): file path
            #   group(2): comment (if present)
            match = re.match(r'^(\S+)\s*(?:"([^"]*)")?', line)
            if match:
                file_path = match.group(1)
                comment = match.group(2) if match.group(2) else ""
                entries.append((file_path, comment))
            else:
                # If the line doesn't match, we can just treat everything as a file path or skip
                # but we'll assume well-formed lines for now.
                continue
    return entries


def read_file_content(file_path):
    """
    Reads file content safely as text (UTF-8), and if that fails,
    as binary (converted to hex).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            return infile.read()
    except UnicodeDecodeError:
        # If UTF-8 decoding fails, try reading as binary
        with open(file_path, 'rb') as infile:
            return infile.read().hex()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def create_template_snapshot(snapshot_path):
    """
    Creates a template snapshot file with example entries if it doesn't exist.
    """
    if os.path.exists(snapshot_path):
        return False
        
    template_content = """# hello_world.py "Outputs Hello World."
# folder/file.py "description"
"""
    with open(snapshot_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    return True


def main(root_directory=None, snapshot_path=None):
    """
    Main function:
    1. Create template snapshot file if it doesn't exist
    2. Parse snapshot file to get list of (file_path, comment)
    3. Read each file from the project root
    4. Combine them into one output file with some basic formatting
    5. Copy the combined content to clipboard
    """
    if root_directory is None:
        root_directory = os.getcwd()
    if snapshot_path is None:
        snapshot_path = os.path.join(root_directory, "snapshot.txt")

    # Create template snapshot file if it doesn't exist
    if create_template_snapshot(snapshot_path):
        print_success(f"Created template snapshot file: {os.path.basename(snapshot_path)}")
        print_info("\nHow to use:")
        print(f"{Fore.WHITE}1. Open {os.path.basename(snapshot_path)} in your text editor")
        print("2. List the files you want to include, one per line")
        print("3. Use relative paths from your current directory")
        print("4. Optionally add comments in quotes after the file path")
        print(f"\nExample format:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  src/main.py \"Main application file\"")
        print(f"  utils/helper.py \"Helper functions\"{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}Run {Fore.CYAN}codesnap{Fore.WHITE} again after adding your files.")
        print(f"The combined code will be saved to {output_file} and copied to your clipboard.{Style.RESET_ALL}")
        return

    # Where to write final output
    output_path = os.path.join(root_directory, output_file)

    # Parse the snapshot file
    snapshot_entries = parse_snapshot_file(snapshot_path)
    
    if not snapshot_entries:
        print_error("No valid entries found in snapshot file.")
        return

    combined_content = ""
    with open(output_path, 'w', encoding='utf-8') as outfile:
        # Go through each entry from snapshot.txt
        print_info("\nProcessing files:")
        for relative_path, comment in snapshot_entries:
            file_path = os.path.join(root_directory, relative_path)
            if os.path.exists(file_path):
                # Create the header
                header = f"--- START FILE: {relative_path} ---\n"
                if comment.strip():
                    header += f"(Comment: {comment.strip()})\n\n"

                # Read the file contents
                content = read_file_content(file_path)
                
                # Create the footer
                footer = f"\n--- END FILE: {relative_path} ---\n\n"

                # Write to file and add to combined content
                outfile.write(header)
                outfile.write(content)
                outfile.write(footer)
                
                # Also add to our string for clipboard
                combined_content += header + content + footer
                
                print(f"{Fore.GREEN}  ✓ {relative_path}{Fore.WHITE}: {comment if comment else 'No comment'}{Style.RESET_ALL}")
            else:
                print_error(f"  {relative_path} does not exist")

    if os.path.exists(output_path):
        # Copy to clipboard
        try:
            pyperclip.copy(combined_content)
            print_success(f"\nSnapshot created: {output_file}")
            print_success("Content copied to clipboard!")
        except Exception as e:
            print_success(f"\nSnapshot created: {output_file}")
            print_error("Failed to copy to clipboard: " + str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Combine scripts listed in a snapshot file into a single file for analysis."
    )
    parser.add_argument(
        "--root",
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        help="Root directory of the project (default: project root directory)"
    )
    parser.add_argument(
        "--snapshot",
        default="snapshot.txt",
        help="Path to the snapshot file listing scripts and comments (default: snapshot.txt)"
    )
    args = parser.parse_args()

    main(args.root, args.snapshot)