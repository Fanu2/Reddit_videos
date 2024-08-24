from moviepy.editor import VideoFileClip

# Path to the input video and output video
input_video_path = "/home/jasvir/Pictures/Jodha/Jodha_with_overlay.mp4"
output_video_path = "/home/jasvir/Pictures/Jodha/Jodha_trimmed.mp4"

# Load the video clip
video_clip = VideoFileClip(input_video_path)

# Define the start and end times for the subclip (in seconds)
start_time = 15
end_time = video_clip.duration

# Trim the video by removing the first 15 seconds
trimmed_clip = video_clip.subclip(start_time, end_time)

# Write the result to a file
trimmed_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')
