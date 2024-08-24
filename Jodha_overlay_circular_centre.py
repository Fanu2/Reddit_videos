import os
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
import numpy as np
from PIL import Image, ImageDraw

# Paths to the input video, audio, and image files
video_path = "/home/jasvir/Pictures/Jodha/jodha.mp4"
audio_path = "/home/jasvir/Pictures/Jodha/jodha.mp3"
image_path = "/home/jasvir/Pictures/Jodha/jodha.png"

# Path to save the output video
output_path = "/home/jasvir/Pictures/Jodha/Jodha_with_overlay.mp4"

# Load the video clip
video_clip = VideoFileClip(video_path)

# Load the audio clip
audio_clip = AudioFileClip(audio_path)

# Get the duration of the audio file
audio_duration = audio_clip.duration

# Calculate how many times the video needs to be looped
num_loops = int(audio_duration / video_clip.duration) + 1

# Loop the video clip to match the audio duration
looped_video = concatenate_videoclips([video_clip] * num_loops).subclip(0, audio_duration)

# Load and resize the image using PIL
image = Image.open(image_path)
original_size = (100, 100)
new_size = (original_size[0] * 2, original_size[1] * 2)  # Double the size
image = image.resize(new_size, Image.LANCZOS)  # Resize the image to desired size
mask_image = Image.new('L', new_size, 0)  # Create a mask with the new size
draw = ImageDraw.Draw(mask_image)
draw.ellipse((0, 0, new_size[0], new_size[1]), fill=255)
mask = np.array(mask_image)

# Convert the image back to a numpy array
image_np = np.array(image)

# Apply the mask to the image
image_np = np.dstack([image_np, mask])

# Create an ImageClip from the masked image
masked_image_clip = ImageClip(image_np).set_duration(audio_duration)

# Set the position of the image overlay to the center
masked_image_clip = masked_image_clip.set_position("center")

# Composite the video with the image overlay
final_clip = CompositeVideoClip([looped_video, masked_image_clip])
final_clip = final_clip.set_audio(audio_clip)

# Write the result to a file
final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
