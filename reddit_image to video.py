import praw
import requests
from PIL import Image
from io import BytesIO
import os
from moviepy.editor import ImageSequenceClip, concatenate_videoclips

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
    Fetch image URLs from multiple Reddit subreddits.

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
            print(f"Fetching from subreddit: {subreddit_name}")
            for submission in subreddit.hot(limit=limit):
                if submission.url.endswith(tuple(image_types)):
                    image_urls.append(submission.url)
                    print(f"Found image: {submission.url}")
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
        image = Image.open(BytesIO(response.content))
        image.save(save_path)
        print(f"Image downloaded: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image {url}: {e}")
    except IOError as e:
        print(f"Failed to save image {url}: {e}")

def resize_image(image_path, output_path, size=(1200, 800)):
    """
    Resize an image to landscape format and save it to the output path.

    Parameters:
    - image_path: Path to the image to resize.
    - output_path: Path to save the resized image.
    - size: Tuple of (width, height) for resizing.
    """
    try:
        with Image.open(image_path) as img:
            # Resize image
            img = img.resize(size, Image.LANCZOS)
            img.save(output_path)
            print(f"Image resized: {image_path}")
    except IOError as e:
        print(f"Failed to resize image {image_path}: {e}")

def create_video_from_images(image_folder, output_file, duration_per_image=6, fps=24):
    """
    Create a video from a sequence of images.

    Parameters:
    - image_folder: Folder containing images.
    - output_file: Path to save the output video.
    - duration_per_image: Duration each image should be displayed in seconds.
    - fps: Frames per second for the video.
    """
    size = (1200, 800)  # Define the common size for all images
    images = [os.path.join(image_folder, img) for img in sorted(os.listdir(image_folder)) if
              img.endswith(('.jpg', '.png'))]

    if not images:
        print("No images found in the specified folder.")
        return

    # Create video from resized images
    clips = []
    for image_path in images:
        image_clip = ImageSequenceClip([image_path], durations=[duration_per_image])
        clips.append(image_clip)

    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.fps = fps  # Set fps for the final clip
    final_clip.write_videofile(output_file, codec='libx264', fps=fps)

def main():
    """Main function to orchestrate the workflow."""
    subreddit_names = ["EarthPorn", "travel", "beautifuldestinations", "naturepics"]
    image_types = ['.jpg', '.png']

    output_dir = '/home/jasvir/PycharmProjects/RedditVideoMakerBot-master/output/output_images'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_urls = fetch_reddit_images(subreddit_names, reddit, image_types, limit=10)
    if not image_urls:
        print("No images found in the subreddits.")
        return

    for i, url in enumerate(image_urls):
        image_path = os.path.join(output_dir, f'image_{i}.jpg')
        download_image(url, image_path)

        # Resize and save the resized image
        resized_path = os.path.join(output_dir, f'image_{i}_resized.jpg')
        resize_image(image_path, resized_path)

    # Create video from resized images
    video_output_file = '/home/jasvir/PycharmProjects/RedditVideoMakerBot-master/output/output_video5.mp4'
    create_video_from_images(output_dir, video_output_file)
    print(f"Video created and saved to: {video_output_file}")

if __name__ == "__main__":
    main()
