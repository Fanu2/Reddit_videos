from moviepy.editor import VideoFileClip, AudioFileClip

# Paths to the input video and audio files
video_path = "/home/jasvir/Pictures/lover/output_video5d.mp4"
audio_path = "/home/jasvir/Pictures/lover/Make You Feel My Love Official Video.mp3"

# Path to save the output video
output_path = "/home/jasvir/Pictures/lover/output_video_with_audio.mp4"

# Time (in seconds) when the audio should start in the video
audio_start_time = 10  # Example: start audio at 10 seconds

# Load the video clip
video_clip = VideoFileClip(video_path)

# Load the audio clip and set its start time
audio_clip = AudioFileClip(audio_path).set_start(audio_start_time)

# Loop the video clip to match the duration of the audio clip
video_clip = video_clip.loop(duration=audio_clip.duration)

# Set the audio of the video clip to the audio clip
final_clip = video_clip.set_audio(audio_clip)

# Write the result to a file
final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
