import praw
import requests
from pathlib import Path
import sys

# Define your Reddit API credentials
REDDIT_CLIENT_ID = 'I5KWMzt16qAvByWv0FEkSg'
REDDIT_CLIENT_SECRET = 'O12GGqh6WDnv0I_sPXO3L0mKOcG1TQ'
REDDIT_USER_AGENT = 'RedditVideoFetcher:1.0 (by /u/singh1021)'

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def fetch_reddit_videos(subreddit_names, reddit_instance, video_types, limit=10):
    """
    Fetch video URLs from multiple Reddit subreddits.

    Parameters:
    - subreddit_names: List of subreddit names to fetch videos from.
    - reddit_instance: Instance of the Reddit API client.
    - video_types: List of video file extensions to consider.
    - limit: Number of videos to fetch per subreddit.
    """
    video_urls = []
    for subreddit_name in subreddit_names:
        try:
            subreddit = reddit_instance.subreddit(subreddit_name)
            print(f"Fetching from subreddit: {subreddit_name}")
            for submission in subreddit.hot(limit=limit):
                print(f"Processing submission: {submission.url}")
                if submission.url.endswith(tuple(video_types)):
                    video_urls.append(submission.url)
                    print(f"Found video: {submission.url}")
        except prawcore.exceptions.Forbidden as e:
            print(f"Forbidden error while accessing subreddit {subreddit_name}: {e}")
        except prawcore.exceptions.RequestException as e:
            print(f"Request error while accessing subreddit {subreddit_name}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    return video_urls

def download_video(url, save_path):
    """
    Download a video from a URL and save it to the given path.

    Parameters:
    - url: URL of the video to download.
    - save_path: Path to save the downloaded video.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Video downloaded: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download video {url}: {e}")

def main(subreddit_names):
    """Main function to orchestrate the workflow."""
    # Update subreddits to more video-centric ones
    subreddit_names = ["videos", "funny", "Documentaries", "comedy", "trendingvideos"]

    # Load video types from the configuration
    video_types = ['.mp4', '.mov', '.avi', '.webm']

    output_dir = Path('/home/jasvir/PycharmProjects/RedditVideoMakerBot-master/output/')
    video_folder = output_dir / 'reddit_videos'

    if not video_folder.exists():
        video_folder.mkdir(parents=True)

    video_urls = fetch_reddit_videos(subreddit_names, reddit, video_types, limit=20)
    if not video_urls:
        print("No videos found in the subreddits.")
        return

    for i, url in enumerate(video_urls):
        save_path = video_folder / f'video_{i}.mp4'
        download_video(url, save_path)

    print(f"Videos downloaded and saved to: {video_folder}")

if __name__ == "__main__":
    main(None)
