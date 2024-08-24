import yt_dlp
import argparse

def download_youtube_video(url, output_path):
    ydl_opts = {
        'outtmpl': output_path,            # Output file path template
        'format': 'best',                  # Download the best quality format available
        'noplaylist': True,                # Only download the single video, not playlists
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',  # User-Agent
        'verbose': True,                  # Enable verbose output
        'nocheckcertificate': True,       # Disable certificate checks
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        print(f"Failed to download video: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos using yt_dlp")
    parser.add_argument("-o", "--output", default="/home/jasvir/Videos/youtube/downloaded_video.mp4", help="Output file path")

    args = parser.parse_args()

    # Prompt the user for the YouTube URL
    url = input("Enter the YouTube video URL: ").strip()

    download_youtube_video(url, args.output)
    print(f"Downloaded video to {args.output}")

if __name__ == "__main__":
    main()
