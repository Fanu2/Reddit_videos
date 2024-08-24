from PIL import Image
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
import os

# Define paths
image_folder = '/home/jasvir/Pictures/lover/'
audio_file = '//home/jasvir/Pictures/lover/Make You Feel My Love Official Video.mp3'
output_video = '//home/jasvir/Pictures/lover/output_video.mp4'
resized_folder = '/home/jasvir/Pictures/Reddit/resized/'

# Create resized folder if it doesn't exist
os.makedirs(resized_folder, exist_ok=True)

# Resize and pad images to the target size
def resize_and_pad(image_path, target_size, output_path):
    with Image.open(image_path) as img:
        # Create a new image with the target size and a white background
        new_img = Image.new('RGB', target_size, (255, 255, 255))
        img.thumbnail((target_size[0], target_size[1]))
        # Calculate padding
        left = (target_size[0] - img.width) / 2
        top = (target_size[1] - img.height) / 2
        new_img.paste(img, (int(left), int(top)))
        new_img.save(output_path)

target_size = (1920, 1080)  # Set target size (width, height)
for img_name in os.listdir(image_folder):
    if img_name.lower().endswith(('.jpg', '.png')):
        img_path = os.path.join(image_folder, img_name)
        resized_path = os.path.join(resized_folder, img_name)
        resize_and_pad(img_path, target_size, resized_path)

# Load resized images
image_files = [os.path.join(resized_folder, img) for img in sorted(os.listdir(resized_folder)) if img.lower().endswith(('.jpg', '.png'))]

# Check if there are images
if len(image_files) == 0:
    raise ValueError("No images found in the resized folder. Please check the folder path and file extensions.")

# Load audio file
audio_clip = AudioFileClip(audio_file)
audio_duration = audio_clip.duration  # Duration of the audio

# Calculate display duration for each image
num_images = len(image_files)
image_duration = audio_duration / num_images  # Duration each image should appear

# Create individual clips for each image
image_clips = []
for img_file in image_files:
    img_clip = ImageSequenceClip([img_file], fps=24).set_duration(image_duration)
    image_clips.append(img_clip)

# Concatenate all image clips
final_clip = concatenate_videoclips(image_clips, method="compose")

# Adjust the final duration to match the audio length
if final_clip.duration < audio_duration:
    # If video is shorter than audio, loop the video to match the audio length
    num_repeats = int(audio_duration / final_clip.duration) + 1
    final_clip = concatenate_videoclips([final_clip] * num_repeats).subclip(0, audio_duration)
elif final_clip.duration > audio_duration:
    # If video is longer than audio, trim the video
    final_clip = final_clip.subclip(0, audio_duration)

# Add audio to video clip
final_clip = final_clip.set_audio(audio_clip)

# Write the final video to a file
final_clip.write_videofile(output_video, codec='libx264', audio_codec='aac')

print(f"Video created successfully and saved to {output_video}")
