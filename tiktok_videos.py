import yt_dlp
import argparse

def download_tiktok_video(url, output_path):
    ydl_opts = {
        'outtmpl': output_path,  # Output file path template
        'format': 'best',        # Download the best quality format available
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    parser = argparse.ArgumentParser(description="Download TikTok videos using yt_dlp")
    parser.add_argument("-o", "--output", default="/home/jasvir/Videos/tiktok/downloaded_video.mp4", help="Output file path")

    args = parser.parse_args()

    # Prompt the user for the TikTok URL
    url = input("Enter the TikTok video URL: ").strip()

    download_tiktok_video(url, args.output)
    print(f"Downloaded video to {args.output}")

if __name__ == "__main__":
    main()
