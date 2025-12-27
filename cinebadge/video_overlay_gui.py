import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
    CompositeVideoClip
)
import numpy as np
from PIL import Image, ImageDraw

class VideoOverlayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Video Overlay Creator")
        self.root.geometry("520x420")
        self.root.resizable(False, False)

        self.video_path = ""
        self.audio_path = ""
        self.image_path = ""
        self.output_path = ""

        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="Video + Audio + Image Overlay",
            font=("Helvetica", 16, "bold")
        )
        title.pack(pady=15)

        self.create_button("Select Video File", self.select_video)
        self.create_button("Select Audio File", self.select_audio)
        self.create_button("Select Image File", self.select_image)
        self.create_button("Select Output File", self.select_output)

        self.status = tk.Label(
            self.root,
            text="Waiting for input files...",
            fg="blue",
            wraplength=450
        )
        self.status.pack(pady=15)

        tk.Button(
            self.root,
            text="🎥 Create Video",
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=8,
            command=self.process_video
        ).pack(pady=20)

    def create_button(self, text, command):
        tk.Button(
            self.root,
            text=text,
            width=30,
            pady=6,
            command=command
        ).pack(pady=5)

    def select_video(self):
        self.video_path = filedialog.askopenfilename(
            filetypes=[("Video Files", "*.mp4 *.mkv *.avi")]
        )
        self.update_status()

    def select_audio(self):
        self.audio_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.mp3 *.wav *.aac")]
        )
        self.update_status()

    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        self.update_status()

    def select_output(self):
        self.output_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4")]
        )
        self.update_status()

    def update_status(self):
        self.status.config(
            text=f"Video: {os.path.basename(self.video_path)}\n"
                 f"Audio: {os.path.basename(self.audio_path)}\n"
                 f"Image: {os.path.basename(self.image_path)}\n"
                 f"Output: {os.path.basename(self.output_path)}"
        )

    def process_video(self):
        if not all([self.video_path, self.audio_path, self.image_path, self.output_path]):
            messagebox.showerror("Missing Files", "Please select all files.")
            return

        try:
            self.status.config(text="Processing video... please wait ⏳")
            self.root.update()

            video_clip = VideoFileClip(self.video_path)
            audio_clip = AudioFileClip(self.audio_path)

            audio_duration = audio_clip.duration
            loops = int(audio_duration / video_clip.duration) + 1

            looped_video = concatenate_videoclips(
                [video_clip] * loops
            ).subclip(0, audio_duration)

            image = Image.open(self.image_path).resize((120, 120), Image.LANCZOS)
            mask_img = Image.new("L", (120, 120), 0)
            draw = ImageDraw.Draw(mask_img)
            draw.ellipse((0, 0, 120, 120), fill=255)

            image_np = np.dstack([np.array(image), np.array(mask_img)])

            image_clip = (
                ImageClip(image_np)
                .set_duration(audio_duration)
                .set_position(("right", "bottom"))
            )

            final_clip = CompositeVideoClip([looped_video, image_clip])
            final_clip = final_clip.set_audio(audio_clip)

            final_clip.write_videofile(
                self.output_path,
                codec="libx264",
                audio_codec="aac"
            )

            messagebox.showinfo("Success", "🎉 Video created successfully!")
            self.status.config(text="Done ✔")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoOverlayApp(root)
    root.mainloop()
