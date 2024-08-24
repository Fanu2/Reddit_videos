import praw
import requests
from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip, concatenate_videoclips
from PIL import Image
from io import BytesIO
import os

# Configuration
REDDIT_SUBREDDIT = 'love'
IMAGE_COUNT = 50  # Adjust as needed
OUTPUT_VIDEO_FILE = '/home/jasvir/Pictures/Reddit/output_video.mp4'
MUSIC_FILE = '/home/jasvir/Pictures/Reddit/mausam.mp3'
IMAGE_SIZE = (1920, 1080)  # Adjust based on your desired resolution
FPS = 24  # Frames per second

# Reddit API setup
reddit = praw.Reddit(
    client_id='I5KWMzt16qAvByWv0FEkSg',
    client_secret='O12GGqh6WDnv0I_sPXO3L0mKOcG1TQ',
    user_agent='RedditImageFetcher:1.0 (by /u/singh1021)'
)

def fetch_images(subreddit_name, count):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        images = []
        for submission in subreddit.hot(limit=count):
            if submission.url.endswith(('jpg', 'jpeg', 'png')):
                try:
                    response = requests.get(submission.url)
                    response.raise_for_status()  # Raise HTTPError for bad responses
                    image = Image.open(BytesIO(response.content))
                    images.append(image)
                except Exception as e:
                    print(f"Failed to fetch or open image: {e}")
        return images
    except praw.exceptions.PRAWException as e:
        print(f"PRAW exception occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request exception occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def resize_images(images, size):
    resized_images = []
    for img in images:
        try:
            img = img.resize(size)
            resized_images.append(img)
        except Exception as e:
            print(f"Failed to resize image: {e}")
    return resized_images

def save_images_as_temp_files(images):
    temp_files = []
    for i, img in enumerate(images):
        temp_file = f'/home/jasvir/Pictures/Reddit/temp_image_{i}.jpg'
        try:
            img.save(temp_file)
            temp_files.append(temp_file)
        except Exception as e:
            print(f"Failed to save image to file: {e}")
    return temp_files

def create_video_from_images(image_files, output_file, duration_per_image=6, fps=24):
    clips = []
    for img_file in image_files:
        try:
            clip = ImageSequenceClip([img_file], durations=[duration_per_image])
            clip.fps = fps  # Set fps for the clip
            clips.append(clip)
        except Exception as e:
            print(f"Failed to create video clip from image: {e}")

    try:
        video = concatenate_videoclips(clips, method='compose')
        video.write_videofile(output_file, codec='libx264', fps=fps)  # Specify fps here
    except Exception as e:
        print(f"Failed to create video file: {e}")

def add_music_to_video(video_file, music_file, output_file):
    if not os.path.exists(video_file):
        print(f"Error: The video file {video_file} was not found. Cannot add music.")
        return

    try:
        video = VideoFileClip(video_file)
        audio = AudioFileClip(music_file).subclip(0, min(video.duration, 60))
        video = video.set_audio(audio)
        video.write_videofile(output_file, codec='libx264')
    except Exception as e:
        print(f"Failed to add music to video: {e}")

def main():
    images = fetch_images(REDDIT_SUBREDDIT, IMAGE_COUNT)
    if images:
        resized_images = resize_images(images, IMAGE_SIZE)
        temp_files = save_images_as_temp_files(resized_images)
        if temp_files:
            create_video_from_images(temp_files, OUTPUT_VIDEO_FILE, fps=FPS)
            add_music_to_video(OUTPUT_VIDEO_FILE, MUSIC_FILE, OUTPUT_VIDEO_FILE)
            # Clean up temporary files
            for file in temp_files:
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"Failed to delete temporary file: {e}")

if __name__ == '__main__':
    main()
