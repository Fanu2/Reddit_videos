import yt_dlp
import argparse

def download_twitter_video(url, output_path):
    ydl_opts = {
        'outtmpl': output_path,  # Output file path template
        'format': 'best',        # Download the best quality format available
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    parser = argparse.ArgumentParser(description="Download Twitter videos using yt_dlp")
    parser.add_argument("-o", "--output", default="/home/jasvir/Videos/twitter/downloaded_video.mp4", help="Output file path")

    args = parser.parse_args()

    # Prompt the user for the Twitter URL
    url = input("Enter the Twitter video URL: ").strip()

    download_twitter_video(url, args.output)
    print(f"Downloaded video to {args.output}")

if __name__ == "__main__":
    main()
