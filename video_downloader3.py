import os
import praw
import requests
from prawcore.exceptions import Redirect

# Define your Reddit API credentials
REDDIT_CLIENT_ID = 'I5KWMzt16qAvByWv0FEkSg'
REDDIT_CLIENT_SECRET = 'O12GGqh6WDnv0I_sPXO3L0mKOcG1TQ'
REDDIT_USER_AGENT = 'RedditImageFetcher:1.0 (by /u/singh1021)'

# Path to save the downloaded videos
video_folder = "/home/jasvir/Pictures/Reddit/videos/"

# Create the folder if it doesn't exist
if not os.path.exists(video_folder):
    os.makedirs(video_folder)

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Function to download Reddit videos
def download_reddit_video(url, path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        return path
    else:
        return None

# Function to download videos from a subreddit
def download_videos(subreddit_name, limit=100):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=limit):
            if submission.is_video and 'reddit_video' in submission.media:
                video_url = submission.media['reddit_video']['fallback_url']
                video_path = os.path.join(video_folder, f"{submission.id}.mp4")
                print(f"Downloading {submission.title}...")
                download_reddit_video(video_url, video_path)
                print(f"Downloaded: {submission.title} to {video_path}")
    except Redirect:
        print(f"Subreddit '{subreddit_name}' not found or invalid.")

# Download videos from the specified subreddit
subreddit_name = 'CatwalkGif'
download_videos(subreddit_name, limit=100)
