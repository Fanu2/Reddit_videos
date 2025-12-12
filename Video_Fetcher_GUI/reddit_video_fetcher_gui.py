"""
Reddit Video Fetcher - Professional GUI
Requirements:
    pip install PySide6 praw requests

Features:
- Enter comma-separated subreddit names
- Configure Reddit credentials (or set via environment variables)
- Set per-subreddit limit and file types
- Start / Stop operations
- Live log, progress bar, and a preview list of found video URLs with checkboxes
- Select output directory
- Runs network operations in a background thread to keep the UI responsive

IMPORTANT: Do NOT hard-code your Reddit client secret in source files. Prefer using environment variables
('REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_USER_AGENT') or paste credentials into the GUI's credential fields.
"""

import os
import sys
import traceback
from pathlib import Path
from typing import List

import praw
import requests
import yt_dlp
from PySide6.QtCore import QThread, Signal, Slot, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QCheckBox,
)

VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.webm']


# --- UPDATED: Added real Reddit video extraction (fallback_url) ---
class FetchDownloadWorker(QThread):
    """Background worker to fetch video URLs and download them.
    Emits signals to update the UI.
    """

    log = Signal(str)
    found_url = Signal(str)
    progress = Signal(int)
    finished_ok = Signal()
    finished_error = Signal(str)

    def __init__(self, reddit_config: dict, subreddits: List[str], limit: int, video_types: List[str], output_dir: str, download_all: bool = True, parent=None):
        super().__init__(parent)
        self.reddit_config = reddit_config
        self.subreddits = [s.strip() for s in subreddits if s.strip()]
        self.limit = limit
        self.video_types = video_types
        self.output_dir = Path(output_dir)
        self._is_stopped = False
        self.download_all = download_all

    def stop(self):
        self._is_stopped = True

    def run(self):
        try:
            self.log.emit("Initializing Reddit client...")
            reddit = praw.Reddit(
                client_id=self.reddit_config.get('client_id'),
                client_secret=self.reddit_config.get('client_secret'),
                user_agent=self.reddit_config.get('user_agent') or 'RedditVideoFetcher:GUI',
            )

            video_urls = []
            total_expected = 0
            for subreddit_name in self.subreddits:
                if self._is_stopped:
                    self.log.emit('Stopped by user.')
                    self.finished_error.emit('Stopped')
                    return
                try:
                    self.log.emit(f"Fetching from subreddit: {subreddit_name}")
                    subreddit = reddit.subreddit(subreddit_name)
                    for submission in subreddit.hot(limit=self.limit):
                        if self._is_stopped:
                            self.log.emit('Stopped by user.')
                            self.finished_error.emit('Stopped')
                            return
                        url = getattr(submission, 'url', '')
                        if not url:
                            continue
                        self.log.emit(f"Found submission URL: {url}")
                        # NEW: Detect Reddit native video
                        if 'v.redd.it' in url:
                            real_url = self._get_reddit_fallback_url(submission)
                            if real_url:
                                video_urls.append(real_url)
                                self.found_url.emit(real_url)
                            continue

                        # NEW: Handle YouTube / FB / TikTok via yt-dlp
                        if any(domain in url for domain in ['youtube.com','youtu.be','facebook.com','fb.watch','tiktok.com','instagram.com']):
                            video_urls.append(url)
                            self.found_url.emit(url)
                            continue

                        # Old behavior for direct MP4 links
                        if url.endswith(tuple(self.video_types)):
                            video_urls.append(url)
                            self.found_url.emit(url)
                except Exception as e:
                    # Log exception but continue with other subreddits
                    self.log.emit(f"Error fetching {subreddit_name}: {e}")

            if not video_urls:
                self.log.emit('No video URLs found.')
                self.finished_ok.emit()
                return

            # ensure output dir exists
            self.output_dir.mkdir(parents=True, exist_ok=True)

            total_expected = len(video_urls)
            self.log.emit(f"Starting downloads: {total_expected} videos")

            for idx, url in enumerate(video_urls, start=1):
                if self._is_stopped:
                    self.log.emit('Stopped by user during downloads.')
                    self.finished_error.emit('Stopped')
                    return
                try:
                    file_suffix = ''.join(Path(url).suffixes) or '.mp4'
                    save_as = self.output_dir / f'video_{idx}{file_suffix}'
                    self.log.emit(f"Downloading ({idx}/{total_expected}): {url} -> {save_as}")
                    # Use yt-dlp for modern platforms
                    if any(x in url for x in ['youtube','youtu.be','facebook','tiktok','instagram']):
                        self._download_with_ytdlp(url, save_as)
                    else:
                        self._download_file(url, save_as)
                    self.progress.emit(int((idx / total_expected) * 100))
                except Exception as e:
                    self.log.emit(f"Failed to download {url}: {e}")

            self.log.emit('All downloads finished.')
            self.progress.emit(100)
            self.finished_ok.emit()

        except Exception as exc:
            tb = traceback.format_exc()
            self.log.emit(f"Fatal error in worker: {exc}\n{tb}")
            self.finished_error.emit(str(exc))

    def _get_reddit_fallback_url(self, submission):
        """Extracts Reddit fallback MP4 URL from post JSON metadata."""
        try:
            post_json = submission._fetch()['secure_media']
            rv = post_json.get('reddit_video') if post_json else None
            if rv and 'fallback_url' in rv:
                return rv['fallback_url']
        except Exception:
            return None
        return None

    def _download_with_ytdlp(self, url: str, save_path: Path):
        opts = {
            'outtmpl': str(save_path),
            'quiet': True,
            'no_warnings': True,
            'format': 'mp4/best',
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

    def _download_file(self, url: str, save_path: Path):
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(save_path, 'wb') as fh:
            for chunk in response.iter_content(chunk_size=8192):
                if self._is_stopped:
                    raise RuntimeError('Stopped')
                if chunk:
                    fh.write(chunk)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Reddit Video Fetcher - Professional GUI')
        self.setMinimumSize(800, 600)
        self._worker = None

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Credentials row
        cred_layout = QHBoxLayout()
        self.client_id_input = QLineEdit(os.getenv('REDDIT_CLIENT_ID', ''))
        self.client_id_input.setPlaceholderText('Reddit client id (or leave empty to use env var)')
        self.client_secret_input = QLineEdit(os.getenv('REDDIT_CLIENT_SECRET', ''))
        self.client_secret_input.setPlaceholderText('Reddit client secret (or leave empty to use env var)')
        self.client_secret_input.setEchoMode(QLineEdit.Password)
        self.user_agent_input = QLineEdit(os.getenv('REDDIT_USER_AGENT', 'RedditVideoFetcher:GUI'))
        self.user_agent_input.setPlaceholderText('User agent')
        cred_layout.addWidget(QLabel('Client ID:'))
        cred_layout.addWidget(self.client_id_input)
        cred_layout.addWidget(QLabel('Secret:'))
        cred_layout.addWidget(self.client_secret_input)
        cred_layout.addWidget(QLabel('User Agent:'))
        cred_layout.addWidget(self.user_agent_input)
        main_layout.addLayout(cred_layout)

        # Subreddits and options
        opts_layout = QHBoxLayout()
        self.subreddits_input = QLineEdit('videos, funny, Documentaries, comedy, trendingvideos')
        self.subreddits_input.setPlaceholderText('Comma-separated list of subreddits')
        self.limit_spin = QSpinBox()
        self.limit_spin.setRange(1, 100)
        self.limit_spin.setValue(20)
        opts_layout.addWidget(QLabel('Subreddits:'))
        opts_layout.addWidget(self.subreddits_input)
        opts_layout.addWidget(QLabel('Limit per subreddit:'))
        opts_layout.addWidget(self.limit_spin)
        main_layout.addLayout(opts_layout)

        # Output folder and controls
        out_layout = QHBoxLayout()
        self.out_dir_label = QLineEdit(str(Path.home() / 'reddit_videos'))
        out_layout.addWidget(QLabel('Output folder:'))
        out_layout.addWidget(self.out_dir_label)
        choose_btn = QPushButton('Browse')
        choose_btn.clicked.connect(self.choose_output_dir)
        out_layout.addWidget(choose_btn)
        main_layout.addLayout(out_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton('Start')
        self.start_btn.clicked.connect(self.start_fetch)
        self.stop_btn = QPushButton('Stop')
        self.stop_btn.clicked.connect(self.stop_fetch)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        main_layout.addLayout(btn_layout)

        # List of found videos
        self.found_list = QListWidget()
        main_layout.addWidget(QLabel('Found video URLs (select which to download if you want):'))
        main_layout.addWidget(self.found_list)

        # Progress and logs
        self.progress_bar = QProgressBar()
        main_layout.addWidget(self.progress_bar)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        main_layout.addWidget(QLabel('Log'))
        main_layout.addWidget(self.log_output, stretch=1)

    @Slot()
    def choose_output_dir(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select output directory', str(Path.home()))
        if folder:
            self.out_dir_label.setText(folder)

    @Slot()
    def start_fetch(self):
        # Read config
        client_id = self.client_id_input.text().strip() or os.getenv('REDDIT_CLIENT_ID')
        client_secret = self.client_secret_input.text().strip() or os.getenv('REDDIT_CLIENT_SECRET')
        user_agent = self.user_agent_input.text().strip() or os.getenv('REDDIT_USER_AGENT', 'RedditVideoFetcher:GUI')

        if not client_id or not client_secret:
            QMessageBox.warning(self, 'Missing credentials', 'Please provide Reddit client id and secret (or set environment variables).')
            return

        subreddits = [s.strip() for s in self.subreddits_input.text().split(',') if s.strip()]
        if not subreddits:
            QMessageBox.warning(self, 'Missing subreddits', 'Please enter at least one subreddit.')
            return

        output_dir = self.out_dir_label.text().strip() or str(Path.home() / 'reddit_videos')
        limit = int(self.limit_spin.value())

        reddit_cfg = {
            'client_id': client_id,
            'client_secret': client_secret,
            'user_agent': user_agent,
        }

        # clear previous results
        self.found_list.clear()
        self.log_output.clear()
        self.progress_bar.setValue(0)

        # disable buttons
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        # start worker thread
        self._worker = FetchDownloadWorker(reddit_cfg, subreddits, limit, VIDEO_EXTENSIONS, output_dir)
        self._worker.log.connect(self.append_log)
        self._worker.found_url.connect(self.add_found_url)
        self._worker.progress.connect(self.progress_bar.setValue)
        self._worker.finished_ok.connect(self.worker_finished_ok)
        self._worker.finished_error.connect(self.worker_finished_error)
        self._worker.start()

    @Slot()
    def stop_fetch(self):
        if self._worker and self._worker.isRunning():
            self.append_log('Stopping...')
            self._worker.stop()
            self.stop_btn.setEnabled(False)

    @Slot(str)
    def append_log(self, message: str):
        self.log_output.append(message)

    @Slot(str)
    def add_found_url(self, url: str):
        # Add a checkboxed list item so user can selectively keep/remove (future enhancement)
        item = QListWidgetItem(url)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked)
        self.found_list.addItem(item)

    @Slot()
    def worker_finished_ok(self):
        self.append_log('Operation completed successfully.')
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    @Slot(str)
    def worker_finished_error(self, message: str):
        self.append_log(f'Operation finished with error: {message}')
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
