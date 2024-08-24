#!/usr/bin/env python
import sys
from pathlib import Path
import praw
import requests
from moviepy.editor import ImageSequenceClip
from PIL import Image
import os
import toml


def load_config():
    """Load configuration from a TOML file."""
    directory = Path().absolute()
    config_path = directory / "config.toml"
    try:
        config = toml.load(config_path)
        # Debug: Print the loaded configuration
        print("Loaded config:", config)
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)


def create_reddit_instance(reddit_config):
    """Create a Reddit instance using the provided configuration."""
    return praw.Reddit(
        client_id=reddit_config.get('client_id', ''),
        client_secret=reddit_config.get('client_secret', ''),
        user_agent=reddit_config.get('user_agent', '')
    )


def fetch_reddit_images(subreddit_name, reddit_instance, limit=10):
    """Fetch images from a Reddit subreddit."""
    subreddit = reddit_instance.subreddit(subreddit_name)
    image_urls = []
    for submission in subreddit.hot(limit=limit):
        if submission.url.endswith(('.jpg', '.jpeg', '.png')):
            image_urls.append(submission.url)
    return image_urls


def download_image(url, save_path):
    """Download an image from a URL and save it to the given path."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download image: {url}")


def resize_image(image_path, output_path, size=(640, 480)):
    """Resize an image to the given size and save it to the output path."""
    with Image.open(image_path) as img:
        img = img.resize(size, Image.LANCZOS)
        img.save(output_path)


def create_video_from_images(image_folder, output_file, fps=24):
    """Create a video from a sequence of images."""
    size = (640, 480)  # Define the common size for all images
    images = [os.path.join(image_folder, img) for img in sorted(os.listdir(image_folder)) if
              img.endswith(('.jpg', '.png'))]

    if not images:
        print("No images found in the specified folder.")
        return

    # Resize images to ensure they are all the same size
    for image_path in images:
        resized_path = image_path.replace('.jpg', '_resized.jpg').replace('.png', '_resized.png')
        resize_image(image_path, resized_path, size)

    resized_images = [img.replace('.jpg', '_resized.jpg').replace('.png', '_resized.png') for img in images]

    # Convert Path objects to strings
    resized_images = [str(Path(img)) for img in resized_images]
    output_file = str(Path(output_file))

    # Create video from resized images
    clip = ImageSequenceClip(resized_images, fps=fps)
    clip.write_videofile(output_file, codec='libx264')


def main(subreddit_name):
    """Main function to orchestrate the workflow."""
    config = load_config()

    if 'reddit' not in config:
        print("Reddit configuration is missing in the config file.")
        sys.exit(1)

    reddit_instance = create_reddit_instance(config['reddit'])

    output_dir = Path('/home/jasvir/PycharmProjects/RedditVideoMakerBot-master/output/')
    image_folder = output_dir / 'reddit_images'
    output_file = output_dir / 'reddit_video.mp4'

    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    image_urls = fetch_reddit_images(subreddit_name, reddit_instance, limit=30)
    if not image_urls:
        print("No images found in the subreddit.")
        return

    for i, url in enumerate(image_urls):
        save_path = image_folder / f'image_{i}.jpg'
        download_image(url, save_path)

    create_video_from_images(image_folder, output_file)
    print(f"Video created and saved to: {output_file}")


def run():
    """Run the main function with exception handling."""
    subreddit_name = "pics"  # Replace with your desired subreddit
    try:
        main(subreddit_name)
    except KeyboardInterrupt:
        print("Process interrupted.")
        sys.exit(0)
    except Exception as err:
        print(f"An error occurred: {err}")
        sys.exit(1)


if __name__ == "__main__":
    if sys.version_info.major != 3 or sys.version_info.minor not in [10, 11]:
        print("This program requires Python 3.10 or 3.11. Please install the correct version of Python.")
        sys.exit(1)

    run()
