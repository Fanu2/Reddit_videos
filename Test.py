import os

# Define the scripts and their filenames
scripts = {
    'file_organizer.py': '''import os
import shutil

def organize_files(source_dir):
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path):
            ext = filename.split('.')[-1]
            target_dir = os.path.join(source_dir, ext)
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(file_path, target_dir)
            print(f"Moved: {filename} to {target_dir}")

if __name__ == "__main__":
    organize_files('/path/to/source_dir')''',

    'file_renamer.py': '''import os

def rename_files(directory, prefix='new_', suffix=''):
    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)
        if os.path.isfile(old_path):
            new_name = prefix + filename + suffix
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} to {new_name}")

if __name__ == "__main__":
    rename_files('/path/to/directory')''',

    'duplicate_finder.py': '''import os
import hashlib

def get_file_hash(file_path):
    hash_algo = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def find_duplicates(directory):
    seen = set()
    duplicates = set()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_hash = get_file_hash(file_path)
            if file_hash in seen:
                duplicates.add(file_path)
            else:
                seen.add(file_hash)

    for duplicate in duplicates:
        os.remove(duplicate)
        print(f"Deleted duplicate: {duplicate}")

if __name__ == "__main__":
    find_duplicates('/path/to/directory')''',

    'directory_sync.py': '''import os
import shutil

def sync_directories(src_dir, dest_dir):
    for filename in os.listdir(src_dir):
        src_file = os.path.join(src_dir, filename)
        dest_file = os.path.join(dest_dir, filename)
        if os.path.isfile(src_file):
            if not os.path.exists(dest_file):
                shutil.copy2(src_file, dest_file)
                print(f"Copied: {filename} to {dest_dir}")

if __name__ == "__main__":
    sync_directories('/path/to/source_dir', '/path/to/dest_dir')''',

    'file_searcher.py': '''import os

def search_files(directory, extension):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                print(os.path.join(root, file))

if __name__ == "__main__":
    search_files('/path/to/directory', '.txt')''',

    'file_backup.py': '''import os
import shutil
from datetime import datetime

def backup_files(directory, backup_dir):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'backup_{timestamp}')
    os.makedirs(backup_path, exist_ok=True)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            shutil.copy2(file_path, backup_path)
            print(f"Backed up: {filename} to {backup_path}")

if __name__ == "__main__":
    backup_files('/path/to/directory', '/path/to/backup_dir')''',

    'file_size_checker.py': '''import os

def file_sizes(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            print(f"{filename}: {size} bytes")

if __name__ == "__main__":
    file_sizes('/path/to/directory')''',

    'file_permission_changer.py': '''import os

def change_permissions(directory, mode):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.chmod(file_path, mode)
            print(f"Changed permissions of: {filename}")

if __name__ == "__main__":
    change_permissions('/path/to/directory', 0o644)''',

    'file_extension_changer.py': '''import os

def change_file_extension(directory, old_ext, new_ext):
    for filename in os.listdir(directory):
        if filename.endswith(old_ext):
            base = filename[:-len(old_ext)]
            new_filename = base + new_ext
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} to {new_filename}")

if __name__ == "__main__":
    change_file_extension('/path/to/directory', '.txt', '.md')''',

    'file_age_checker.py': '''import os
import time

def check_file_age(directory, days):
    cutoff = time.time() - days * 86400
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if os.path.getmtime(file_path) < cutoff:
                print(f"{filename} is older than {days} days")

if __name__ == "__main__":
    check_file_age('/path/to/directory', 30)'''
}

# Path to the project directory
project_dir = '/home/jasvir/PycharmProjects/pythonProject2/'

# Create the files
for filename, content in scripts.items():
    file_path = os.path.join(project_dir, filename)
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"Created: {file_path}")
