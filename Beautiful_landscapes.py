import praw
import os
import requests
from PIL import Image
from moviepy.editor import ImageSequenceClip

# Define your Reddit API credentials
REDDIT_CLIENT_ID = 'I5KWMzt16qAvByWv0FEkSg'
REDDIT_CLIENT_SECRET = 'O12GGqh6WDnv0I_sPXO3L0mKOcG1TQ'
REDDIT_USER_AGENT = 'RedditImageFetcher:1.0 (by /u/singh1021)'

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Path for saving images
image_path = '/home/jasvir/Pictures/Reddit/images'
if not os.path.exists(image_path):
    os.makedirs(image_path)

# Resize and save image
def resize_image(image_path, size):
    with Image.open(image_path) as img:
        img = img.convert('RGB')  # Convert image to RGB mode
        img = img.resize(size, Image.LANCZOS)
        img.save(image_path)

# Fetch images from subreddit
subreddit = reddit.subreddit('SexyButClothed')
images = []
target_size = (680, 680)  # Adjust target size as needed

print("Fetching images from subreddit...")

for submission in subreddit.hot(limit=200):  # Adjust the limit as needed
    if submission.url.endswith(('.jpg', '.jpeg', '.png')):
        print(f"Processing image URL: {submission.url}")
        image_url = submission.url
        image_name = os.path.join(image_path, f"{submission.id}.jpg")
        try:
            with open(image_name, 'wb') as image_file:
                image_file.write(requests.get(image_url).content)
            resize_image(image_name, target_size)
            images.append(image_name)
        except Exception as e:
            print(f"Failed to process image URL: {submission.url} - Error: {e}")

if not images:
    print("No images found or downloaded.")
else:
    # Create a video from the images
    clip = ImageSequenceClip(images, fps=1)  # Adjust fps as needed
    clip.write_videofile('/home/jasvir/Pictures/Reddit/output_video5p.mp4')
