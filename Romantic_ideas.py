import praw
import requests
from moviepy.editor import ImageSequenceClip
from PIL import Image
import os
import sys
from pathlib import Path
import prawcore  # Import prawcore to handle specific exceptions

# Define your Reddit API credentials
REDDIT_CLIENT_ID = 'I5KWMzt16qAvByWv0FEkSg'
REDDIT_CLIENT_SECRET = 'O12GGqh6WDnv0I_sPXO3L0mKOcG1TQ'
REDDIT_USER_AGENT = 'RedditImageFetcher:1.0 (by /u/singh1021)'

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)


def fetch_reddit_images(subreddit_names, reddit_instance, image_types, limit=10):
    """
    Fetch images from multiple Reddit subreddits.

    Parameters:
    - subreddit_names: List of subreddit names to fetch images from.
    - reddit_instance: Instance of the Reddit API client.
    - image_types: List of image file extensions to consider.
    - limit: Number of images to fetch per subreddit.
    """
    image_urls = []
    for subreddit_name in subreddit_names:
        try:
            subreddit = reddit_instance.subreddit(subreddit_name)
            for submission in subreddit.hot(limit=limit):
                if any(submission.url.endswith(img_type) for img_type in image_types):
                    image_urls.append(submission.url)
        except prawcore.exceptions.Forbidden as e:
            print(f"Forbidden error while accessing subreddit {subreddit_name}: {e}")
        except prawcore.exceptions.RequestException as e:
            print(f"Request error while accessing subreddit {subreddit_name}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    return image_urls


def download_image(url, save_path):
    """
    Download an image from a URL and save it to the given path.

    Parameters:
    - url: URL of the image to download.
    - save_path: Path to save the downloaded image.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image {url}: {e}")


def resize_image(image_path, output_path, size=(640, 480)):
    """
    Resize an image to the given size and save it to the output path.

    Parameters:
    - image_path: Path to the image to resize.
    - output_path: Path to save the resized image.
    - size: Tuple of (width, height) for resizing.
    """
    try:
        with Image.open(image_path) as img:
            img = img.resize(size, Image.Resampling.LANCZOS)
            img.save(output_path)
    except Exception as e:
        print(f"Failed to resize image {image_path}: {e}")


def create_video_from_images(image_folder, output_file, fps=.5):
    """
    Create a video from a sequence of images.

    Parameters:
    - image_folder: Folder containing images.
    - output_file: Path to save the output video.
    - fps: Frames per second for the video.
    """
    size = (640, 480)  # Define the common size for all images
    images = [str(image_folder / img) for img in sorted(os.listdir(image_folder)) if
              img.endswith(('.jpg', '.png'))]

    if not images:
        print("No images found in the specified folder.")
        return

    # Resize images to ensure they are all the same size
    resized_images = []
    for image_path in images:
        resized_path = image_path.replace('.jpg', '_resized.jpg').replace('.png', '_resized.png')
        resize_image(image_path, resized_path, size)
        resized_images.append(resized_path)

    # Create video from resized images
    try:
        clip = ImageSequenceClip(resized_images, fps=fps)
        clip.write_videofile(str(output_file), codec='libx264')
    except Exception as e:
        print(f"Failed to create video: {e}")


def main(subreddit_names):
    """Main function to orchestrate the workflow."""
    config = {
        'reddit': {
            'client_id': REDDIT_CLIENT_ID,
            'client_secret': REDDIT_CLIENT_SECRET,
            'user_agent': REDDIT_USER_AGENT
        },
        'background': {
            'video': {},
            'audio': {}
        }
    }

    # Load image types from the configuration
    image_types = ['.jpg', '.png']

    output_dir = Path('/home/jasvir/PycharmProjects/RedditVideoMakerBot-master/output/')
    image_folder = output_dir / 'reddit_images'
    output_file = output_dir / 'reddit_video4.mp4'

    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    image_urls = fetch_reddit_images(subreddit_names, reddit, image_types, limit=50)
    if not image_urls:
        print("No images found in the subreddits.")
        return

    for i, url in enumerate(image_urls):
        save_path = image_folder / f'image_{i}.jpg'
        download_image(url, save_path)

    create_video_from_images(image_folder, output_file)
    print(f"Video created and saved to: {output_file}")


if __name__ == "__main__":
    subreddit_names = ["beautiful", "Love", "TrueRomance"]  # Replace with desired subreddits
    if sys.version_info.major != 3 or sys.version_info.minor not in [10, 11]:
        print("This program requires Python 3.10 or 3.11. Please install the correct version of Python.")
        sys.exit(1)

    main(subreddit_names)
