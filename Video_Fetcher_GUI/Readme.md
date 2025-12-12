# Reddit Video Fetcher GUI

A powerful, user‑friendly desktop application for downloading videos from **Reddit**, **YouTube**, **Facebook**, **TikTok**, **Instagram**, and more. Built with **PySide6**, **PRAW**, and **yt‑dlp**, this tool allows you to fetch posts from multiple subreddits, preview found URLs, and download videos seamlessly.

---

## 🚀 Features

### 🔎 Fetch Videos from Multiple Subreddits

* Enter any number of comma‑separated subreddit names.
* Fetches posts via Reddit's API using **PRAW**.
* Automatically detects:

  * Reddit-native videos (`v.redd.it`)
  * YouTube links
  * Facebook video links
  * TikTok & Instagram links
  * Direct MP4 links

### 🎬 Smart Video Detection

* Extracts the **fallback MP4 URL** from Reddit posts (DASH video).
* Identifies downloadable links using **yt‑dlp** for external platforms.

### 📥 Download Videos Easily

* Downloads Reddit videos directly.
* Uses *yt-dlp* for YouTube, Facebook, TikTok, Instagram, and many other platforms.
* Saves all videos in a user-selected output directory.

### 🖥 Polished GUI Built With PySide6

* Subreddit input field
* Credential fields (with environment variable fallback)
* Output folder chooser
* Live logging window
* Progress bar
* URL list with checkboxes
* Start/Stop controls

### 🧵 Non‑Blocking Downloads

Runs all network operations inside a **background worker thread**, keeping the GUI responsive.

---

## 📦 Requirements

Install the required Python packages:

```bash
pip install PySide6 praw requests yt-dlp
```

### Optional (Recommended)

To avoid hard‑coding credentials, export these environment variables:

```bash
export REDDIT_CLIENT_ID="your_id"
export REDDIT_CLIENT_SECRET="your_secret"
export REDDIT_USER_AGENT="YourAppName:1.0"
```

---

## 🔧 Configuration

### Reddit API Credentials

You must create an app here:

[https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)

Use

* **script** application type
* Redirect URL: `http://localhost`

Then copy:

* `client_id`
* `client_secret`
* `user_agent`

You may enter these in the GUI or set environment variables.

---

## ▶️ Running the Application

Simply run:

```bash
python reddit_video_fetcher_gui.py
```

The GUI will launch.

---

## 📂 Output

Downloaded videos are saved into the output directory you specify.

Filenames follow this pattern:

```
video_1.mp4
video_2.mp4
video_3.mp4
...
```

Reddit videos may use various resolutions depending on the fallback file available.

---

## 🧠 How Video Detection Works

### 1. **Reddit Native Videos (`v.redd.it`)**

* Fetches submission JSON metadata.
* Extracts:

  ```python
  secure_media.reddit_video.fallback_url
  ```
* This provides a direct MP4 download.

### 2. **Direct Video Files**

Works when URLs end with:

```
.mp4 .webm .mov .avi
```

### 3. **External Platforms**

Anything containing:

```
youtube, youtu.be, facebook, fb.watch, tiktok, instagram
```

is passed to **yt-dlp**.

---

## 🛠 Architecture Overview

```
GUI (PySide6)
│
├── MainWindow
│   ├── Inputs (subreddits, credentials, output folder)
│   ├── Buttons (Start, Stop)
│   ├── Log display
│   └── List of found URLs
│
└── FetchDownloadWorker (QThread)
    ├── Fetches posts from Reddit
    ├── Extracts valid video URLs
    ├── Uses yt-dlp when needed
    ├── Downloads files
    └── Emits progress/log updates
```

---

## 🧩 Troubleshooting

| Issue                        | Cause                                             | Fix                                   |
| ---------------------------- | ------------------------------------------------- | ------------------------------------- |
| `No module named PySide6`    | Dependency missing                                | Run `pip install PySide6`             |
| `Invalid Reddit credentials` | Wrong `client_id` or `secret`                     | Verify app settings on Reddit         |
| `No video URLs found`        | Posts contained only external or unsupported URLs | Add yt-dlp support (already included) |
| Videos not downloading       | Missing write permissions                         | Choose a different output folder      |

---

## 🗺 Planned Enhancements

* [ ] Download only selected URLs
* [ ] Show video thumbnails
* [ ] Auto-merge Reddit DASH video + audio with FFmpeg
* [ ] Parallel downloads
* [ ] Custom yt-dlp format selector
* [ ] Dark/Light UI themes

---

## 🤝 Contributing

Pull requests and feature ideas are welcome!

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙌 Acknowledgments

* **Reddit API (PRAW)** — for subreddit content fetching
* **yt-dlp** — incredible video downloader engine
* **PySide6** — modern Python GUI framework
