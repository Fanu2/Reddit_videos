import os
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
from PIL import Image

# Paths to the input video, audio, and image files
video_path = "/home/jasvir/Pictures/Jodha/jodha.mp4"
audio_path = "/home/jasvir/Pictures/Jodha/jodha.mp3"
image_path = "/home/jasvir/Pictures/Jodha/jodha.png"

# Path to save the output video
output_path = "/home/jasvir/Pictures/Jodha/output_video_with_overlay.mp4"

# Resize image function
def resize_image(input_image_path, output_image_path, height=200):
    img = Image.open(input_image_path)
    aspect_ratio = img.width / img.height
    new_width = int(aspect_ratio * height)
    img = img.resize((new_width, height), Image.LANCZOS)
    img.save(output_image_path)
    return output_image_path

# Resize the image and save it
resized_image_path = "/home/jasvir/Pictures/Jodha/resized_roses1.jpeg"
resize_image(image_path, resized_image_path)

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

# Load the resized image clip and set its position
image_clip = ImageClip(resized_image_path).set_duration(audio_duration)
image_clip = image_clip.set_position(("right", "bottom"))

# Composite the video with the image overlay
final_clip = CompositeVideoClip([looped_video, image_clip])
final_clip = final_clip.set_audio(audio_clip)

# Write the result to a file
final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
