import os
import fnmatch

# File types to be collected
include_file_types = ['*.py', '*.txt','*.html', '*.json','*.css', '*.js']

# File types and directories to be excluded
exclude_file_types = ['*.zip', '*.pyc', '*.log',
                      'Concatenated_files.txt',
                      'code_concatenator.py', #exclude this file
                      'README.md',
                      'LICENSE.txt']

exclude_dirs = ['env', 
                '.git', 
                '.vscode', 
                '__pycache__']

def print_dir_tree(directory, output_file, level=0):
    indent = ' ' * 4 * level
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path) and item not in exclude_dirs:
                output_file.write(f"{indent}Directory: {item}\n")
                print_dir_tree(item_path, output_file, level + 1)
    except Exception as e:
        output_file.write(f"Error while listing directory {directory}: {e}\n")

def print_files(directory, output_file):
    try:
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if any(fnmatch.fnmatch(file, pattern) for pattern in include_file_types) and not any(fnmatch.fnmatch(file, pattern) for pattern in exclude_file_types):
                    file_path = os.path.join(root, file)
                    output_file.write(f"\nFile: {file_path}\n")
                    try:
                        with open(file_path, "r") as file_to_include:
                            output_file.write(file_to_include.read())
                            output_file.write("\n")
                    except Exception as e:
                        output_file.write(f"Error reading file {file_path}: {e}\n")
    except Exception as e:
        output_file.write(f"Error while walking directory {directory}: {e}\n")

# Directory to be collected
directory = "."

with open("Concatenated_files.txt", "w") as output_file:
    output_file.write("Project Tree:\n")
    print_dir_tree(directory, output_file)
    output_file.write("\nFiles:\n")
    print_files(directory, output_file)
