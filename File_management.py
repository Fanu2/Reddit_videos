import os
import shutil

# Define source and destination directories
source_dir = '/home/jasvir/Videos/'
destination_dir = os.path.join(source_dir, 'media')

# Create destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# Move all .mp4 and .webm files to the new folder
for filename in os.listdir(source_dir):
    if filename.endswith('.mp4') or filename.endswith('.webm'):
        file_path = os.path.join(source_dir, filename)
        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            shutil.move(file_path, destination_dir)
            print(f"Moved: {filename}")

print("Files moved successfully.")
